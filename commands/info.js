const { SlashCommandBuilder, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');
const packageJson = require('../package.json');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('info')
        .setDescription('ℹ️ Get information about the bot.'),
    async execute(interaction) {
        const embed = new EmbedBuilder()
            .setColor(0x00FF00)
            .setTitle('ℹ️ Bot Information')
            .addFields(
                { name: 'Name', value: "HitRadio" },
                { name: 'Coded with', value: "JavaScript" },
                { name: 'Description', value: packageJson.description },
                { name: 'Version', value: packageJson.version },
                { name: 'Made by', value: packageJson.author + " < and with ❤️" },
            );

        const row = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setLabel('Support')
                    .setStyle(ButtonStyle.Link)
                    .setEmoji('🆘')
                    .setURL('https://discord.com/invite/MfR5mcpVfX')
            );

        await interaction.reply({ embeds: [embed], components: [row], ephemeral: true });
    },
};
