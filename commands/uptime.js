const { SlashCommandBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('uptime')
        .setDescription('⏱️ Check the bot\'s uptime.'),
    async execute(interaction) {
        const uptime = process.uptime();
        const hours = Math.floor(uptime / 3600);
        const minutes = Math.floor((uptime % 3600) / 60);
        const seconds = Math.floor(uptime % 60);

        const embed = {
            color: 65280,
            description: `⏱️ Uptime: **${hours}h ${minutes}m ${seconds}s**`,
        };
        await interaction.reply({ embeds: [embed], ephemeral: true });
    },
};
