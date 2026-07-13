const { Client, GatewayIntentBits, EmbedBuilder } = require("discord.js");

const intents = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.GuildMessages,
  ],
});

const MEMBER_ROLE_NAME = "MEMBERS";

function clean(text) {
  return text
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase();
}

intents.once("ready", () => {
  console.log(`Logged in as ${intents.user.tag} (ID: ${intents.user.id})`);
  console.log("Bot is ready and watching for new members...");
});

intents.on("guildMemberAdd", async (member) => {
  const role = member.guild.roles.cache.find((r) => r.name === MEMBER_ROLE_NAME);
  if (role) {
    try {
      await member.roles.add(role, "Auto-assigned Member role on join");
    } catch (err) {
      if (err.code !== 50013) console.error(err);
    }
  }

  for (const ch of member.guild.channels.cache.values()) {
    if (ch.isTextBased() && clean(ch.name).includes("wel")) {
      const embed = new EmbedBuilder()
        .setTitle("Welcome!")
        .setDescription(
          `Hey ${member}, welcome to **${member.guild.name}**!\nYou are member #${member.guild.memberCount}.`
        )
        .setColor(0x2ecc71)
        .setThumbnail(member.displayAvatarURL());
      await ch.send({ embeds: [embed] });
      return;
    }
  }
  console.log(`No welcome channel found in ${member.guild.name}`);
});

intents.on("guildMemberRemove", async (member) => {
  for (const ch of member.guild.channels.cache.values()) {
    if (ch.isTextBased() && clean(ch.name).includes("lea")) {
      const embed = new EmbedBuilder()
        .setTitle("Goodbye!")
        .setDescription(`**${member.user.username}** has left the server.`)
        .setColor(0xe74c3c)
        .setThumbnail(member.displayAvatarURL());
      await ch.send({ embeds: [embed] });
      return;
    }
  }
  console.log(`No leave channel found in ${member.guild.name}`);
});

const TOKEN = process.env.DISCORD_TOKEN || "";
intents.login(TOKEN);
