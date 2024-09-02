const { SlashCommandBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('vote')
        .setDescription('🗳️ Vote for the bot.'),
    async execute(interaction) {
        const row = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setLabel('Vote on Top.gg')
                    .setStyle(ButtonStyle.Link)
                    .setEmoji('💖')
                    .setURL('https://top.gg/bot/1086030727650476153'),
                new ButtonBuilder()
                    .setLabel('Invite to your Server')
                    .setStyle(ButtonStyle.Link)
                    .setEmoji('➕')
                    .setURL('https://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands')
            );

        const embed = {
            title: ':heart: Vote for the Bot',
            color: 65280,
            description: '🗳️ Voting for the Bot makes it more known.',
        };

        await interaction.reply({ embeds: [embed], components: [row], ephemeral: true });
    },
};
