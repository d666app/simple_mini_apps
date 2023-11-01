# Examples of Mini Apps for Telegram Mini App Contest
![image](https://i.imgur.com/1uLVZ6X.png)

1. [Telegram Mini Apps Showcase](#telegram-mini-apps-showcase)
2. [Prerequisites](#prerequisites)
3. [Setting Up Your Telegram Bot](#setting-up-your-telegram-bot)
    - [Installation Steps](#installation-steps)
4. [Configuring Your Domain and SSL/TLS Certificate](#configuring-your-domain-and-ssltls-certificate)
5. [Keyboard Button Mini App](#keyboard-button-mini-app)
6. [Inline Button Mini Apps](#inline-button-mini-apps)
    - [Example: Configuring Mini App Buttons](#example-configuring-mini-app-buttons)
7. [How Mini Apps Work](#how-mini-apps-work)
    - [Server-Side Verification](#server-side-verification)
8. [Customizing User Interface](#customizing-user-interface)
    - [MainButton](#mainbutton)
    - [Sending Data to the Bot](#sending-data-to-the-bot)
    - [BackButton](#backbutton)
    - [Handling Bot Updates](#handling-bot-updates)
    - [Alerts and Popups](#alerts-and-popups)
9. [Additional Features](#additional-features)
    - [Haptic Feedback](#haptic-feedback)
    - [Cloud Storage](#cloud-storage)
    - [QR Code Scanning](#qr-code-scanning)

---

# Telegram Mini Apps Showcase

Welcome to the Telegram Mini App Showcase for the Telegram Mini App Contest! These mini apps showcase the various functionality and creativity of the Telegram ecosystem. Whether you're a beginner or an experienced developer, these mini-apps offer a wide range of features that you can explore.

## Prerequisites

Before diving into these mini apps, make sure you have Python of one of the latest versions installed on your system. The great thing about these mini apps is that they don't require any additional libraries or dependencies through the console. So, let's get started!

## Setting Up Your Telegram Bot

To experience these mini apps, you'll need to create a Telegram bot and obtain its token from [@BotFather](https://t.me/BotFather). You can add this token to the `config.py` file or provide it when running `server.py`.

### Installation Steps

Choose the appropriate instructions for your Linux distribution:

- **For Ubuntu 22.04:**
  ```bash
  git clone https://github.com/d666app/simple_mini_apps
  cd simple_mini_apps
  python3 server.py
  ```

- **For Debian 12 and Astra Linux CE 2.12:**
  ```bash
  sudo apt install git
  git clone https://github.com/d666app/simple_mini_apps
  cd simple_mini_apps
  python3 server.py
  ```

- **For CentOS 8:**
  ```bash
  sudo yum install git
  git clone https://github.com/d666app/simple_mini_apps
  cd simple_mini_apps
  python3 server.py
  ```

## Configuring Your Domain and SSL/TLS Certificate

To display your mini-application on Telegram, you'll need a domain accessible via HTTPS. You can purchase a domain from services like Google Domains or reg.ru (for Russians). After obtaining a domain, add it to cloudflare.com to obtain a free SSL/TLS certificate.

You can specify the registered domain when running `server.py` or update the values in `config.py`.

## Keyboard Button Mini App

At this point, you'll have a Keyboard Button Mini App for ordering food ready to use. This mini app provides a user-friendly way to place food orders.

![Keyboard Button Mini App](https://core.telegram.org/file/464001388/10b1a/IYpn0wWfggw.1156850/fd9a32baa81dcecbe4)

You can also create a Mini App accessible from the menu button by following these steps:

- Send the `/mybots` command to BotFather.
- Select your bot from the list and choose the "Bot Settings" option.
- Select the "Menu button" option.
- Select the "Edit menu button URL" option and provide the URL of your Telegram Mini App, such as `https://your-domain/mini-game`.

## Inline Button Mini Apps

To enable Inline Button Mini Apps (notes, casino, music, wallet), you need to create a new app using the `/newapp` command in the same bot with [@botfather](https://t.me/BotFather). There are also commands to manage these apps:

- `/myapps`: Edit your mini apps.
- `/newapp`: Create a new mini app.
- `/listapps`: Get a list of your mini apps.
- `/editapp`: Edit a mini app.
- `/deleteapp`: Delete an existing mini app.

You'll need to create four Mini Apps for notes, casino, music, and wallet. In the URL, specify one of the HTML files from the public folder (e.g., `https://your-domain/notes`) and indicate the app's title accordingly.

### Example: Configuring Mini App Buttons

In your [bot.py](https://github.com/d666app/simple_mini_apps/blob/main/bot.py), you can configure Mini App buttons as follows:

```python
webapp_keyboard = json.dumps({'inline_keyboard': [
    [{"text": "🧠 Notes", "url": f"https://t.me/{bot_username}/notes?startapp"},
     {"text": "🎰 Casino", "url": f"https://t.me/{bot_username}/casino?startapp"}],
    [{"text": "🎧 Music", "url": f"https://t.me/{bot_username}/music?startapp"},
     {"text": "👛 Wallet", "url": f"https://t.me/{bot_username}/wallet?startapp"}]
]})
```

## How Mini Apps Work

Telegram mini-apps allow you to interact with Telegram data and features. To get started, the following script has been included in each file in [public directory](https://github.com/d666app/simple_mini_apps/tree/main/public):

```html
<script src="https://telegram.org/js/telegram-web-app.js"></script>
```

After adding this script, you can customize your mini app's elements based on the Telegram user's theme colors. You can use the provided color variables in your CSS and JavaScript code.

### Available Color Variables

In CSS:
- `var(--tg-theme-bg-color)`
- `var(--tg-theme-text-color)`
- `var(--tg-theme-hint-color)`
- `var(--tg-theme-link-color)`
- `var(--tg-theme-button-color)`
- `var(--tg-theme-button-text-color)`

In JavaScript:
```javascript
let tg = window.Telegram.WebApp;

tg.themeParams.bg_color
tg.themeParams.text_color
tg.themeParams.hint_color
tg.themeParams.link_color
tg.themeParams.button_color
tg.themeParams.button_text_colorString
```

To access Telegram user data, use `initDataUnsafe`. Note that this parameter should be trusted only after server-side verification using a bot token. You can find the verification process in [server.py](https://github.com/d666app/simple_mini_apps/blob/main/server.py).

### Server-Side Verification

```python
def validate_hash(hash_str, init_data, token, c_str="WebAppData"):
    # Parse and sort the initialization data
    init

_data = sorted([chunk.split("=")
                        for chunk in unquote(init_data).split("&")
                        if not chunk.startswith("hash=")],
                       key=lambda x: x[0])
    init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])

    # Generate the secret key and perform HMAC validation
    secret_key = hmac.new(c_str.encode(), token.encode(),
                         hashlib.sha256).digest()
    data_check = hmac.new(secret_key, init_data.encode(),
                          hashlib.sha256)

    return data_check.hexdigest() == hash_str
```

## Customizing User Interface

Telegram allows you to customize the user interface, including MainButtons, BackButtons, alerts and pop-ups. You can make your mini-application stand out and enhance the user experience.

### MainButton

The MainButton can be used to display important information to users. You can show or hide it, change its text, and control its interactivity.

Example in [order-food.html](https://github.com/d666app/simple_mini_apps/blob/main/public/order-food.html):

```javascript
tg.MainButton.show();
tg.MainButton.text = "You haven't chosen any products";
tg.MainButton.hide();
```

We can also change the isActive parameter, which, for example, prevents the user from pressing the MainButton while the roulette wheel in the mini-casino is spinning : ` tg.MainButton.isActive = false;`

### Sending Data to the Bot

You can send data directly from the Mini App to the bot. This can be combined with MainButton but is not mandatory.

[order-food.html](https://github.com/d666app/simple_mini_apps/blob/main/public/order-food.html)
```javascript
Telegram.WebApp.onEvent('mainButtonClicked', function(){
    orderData = calculateAndLogTotalCost();
    const orderText = "You have successfully placed an order:\n\n" + orderData[0].join('\n') + `\n\nTotal: $${orderData[1]}`;
    console.log(orderText);
    // Send the order message using the tg.sendData() method
    tg.sendData(orderText);
});
```

### BackButton

The BackButton works the same way as the MainButton. You can hide and show these two buttons by changing the `isVisible` parameter.

Example: `backButton.isVisible = true;`

### Handling Bot Updates

After executing `tg.sendData`, the bot receives an update with the 'web_app_data' parameter, which can be processed in your [bot.py](https://github.com/d666app/simple_mini_apps/blob/main/bot.py).

```python
elif 'web_app_data' in message:
    send_message(chat_id, message['web_app_data']['data'])
```

### Alerts and Popups

You can send alerts and create pop-up dialogs for various user interactions.

Example:

- Alert: `tg.showAlert("Please enter note text.");`
- Popup: `tg.showPopup({"title":"LOSE","message":"No match. You lost 10 points."});`

An example of a more complex popup. We ask the user to confirm if they really want to delete the note:

[notes.html](https://github.com/d666app/simple_mini_apps/blob/53e14586a5fd5f82fb5518258fc5d867e30bfe69/public/notes.html#L157)
```javascript
const popupParams = {
    title: "Confirmation",
    message: "Are you sure you want to delete this note?",
    buttons: [
        {
            type: "destructive",
            text: "Yes",
            id: "confirmDelete"
        },
        {
            type: "close",
            text: "Cancel",
            id: "cancelDelete"
        }
    ]
};

tg.showPopup(popupParams, ...)
```

## Additional Features

Telegram offers additional features, such as haptic feedback options and cloud storage for your Mini Apps. These features can enhance user engagement and functionality.

### Haptic Feedback

You can trigger tactile effects on the user's smartphone to provide a more immersive experience. [Learn more](https://core.telegram.org/bots/webapps#hapticfeedback).

[mini-casino.html](https://github.com/d666app/simple_mini_apps/blob/53e14586a5fd5f82fb5518258fc5d867e30bfe69/public/mini-casino.html#L122-L130)
```javascript

    if (slot1 === slot2 && slot2 === slot3) {
        balance += 1000;
        updateBalance();
        tg.showPopup({"title":"WIN","message":"You won 1000 points!"});
        tg.HapticFeedback.notificationOccurred('success');
    } else {
        tg.showPopup({"title":"LOSE","message":"No match. You lost 10 points."});
        tg.HapticFeedback.notificationOccurred('error');
    }

```

### Cloud Storage

CloudStorage is an option that allows Mini Apps to store data in the cloud. This feature is useful for applications that aim to work without a backend. You can use it to store user preferences and data. For example, we can store Mini App data for notes in CloudStorage rather than on our own server. I used it in a music application to show the user which songs they liked or disliked

Example usage in [music.html](https://github.com/d666app/simple_mini_apps/blob/main/public/music.html):

```javascript
tg.CloudStorage.getItem(`dislike_${songId}`, ...)
tg.CloudStorage.setItem(`like_${songId}`, true, ...)
tg.CloudStorage.removeItem(`dislike_${songId}`, ...)
```

### QR Code Scanning

You can implement QR code scanning in your Mini App. For example, in the wallet app, you can use the `ScanQrPopup` to expedite the entry of wallet IDs.

Example in [mini-wallet.html](https://github.com/d666app/simple_mini_apps/blob/main/public/mini-wallet.html):

```javascript
tg.showScanQrPopup(params, function(qrText) {
    // Handle the QR code text received
    if (qrText) {
        // Close the QR scanner popup
        tg.closeScanQrPopup();

        // Set the scanned user ID in the input field
        document.getElementById("user-id").value = qrText;
    }
});
```
