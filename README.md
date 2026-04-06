# Queue Eliminator
**Queue Eliminator** is a web application designed to eliminate long waiting lines at places like banks, hospitals, and government offices simply by scanning a **QR code**. 


### 💡 The Problem We All Face

We’ve all been there. Standing in a long queue at a bank. Sitting for hours in a hospital lobby. Waiting endlessly at a government office or even a barber shop just for your number to be called.

***Most of that time? Completely wasted.***

You can’t leave because you might miss your turn. So you just sit there, watching numbers move slowly, feeling stuck and unproductive.

### ✨ What If It Was Different?

*What if you didn’t have to physically stand in line?*

**With Queue Eliminator, you simply:**

- Scan a QR code at the location
- Fill out a quick form (if required)
- *`Join the queue digitally`*

Now instead of waiting in one place, you’re free.

- Go grab a coffee ☕
- Finish your errands 🛒
- Get some fresh air 🌿

Meanwhile, **Queue Eliminator keeps you updated with:**

- 📍 Your live position in the queue
- ⏰ Real-time updates
- 🔔 Alerts before your turn arrives


### 🎯 The Goal

To give people back their time, reduce frustration, and make waiting smarter, not longer.

## ⚙️ How It Works
### 1) Admin Registration
- The admin signs up on our platform and sets up their service (bank, hospital, office, etc.).
### 2) Create a Custom Form
- Based on their requirements, the admin creates a simple form to collect necessary details from users.
### 3) Generate QR Code
- Once the form is ready, the system generates a unique link along with a QR code.
### 4) User Joins the Queue
- Customers simply scan the QR code, fill out the form (if required), and instantly secure their spot in the queue, without standing in line.

## ✨ Features
### 👨‍💼 Admin
- 📊 **Real-Time Dashboard & Analytics**
    - Monitor key metrics like total clients, skipped clients, and missed clients within a selected time range.
- 🤝 **Add Coordinators**
-   - Invite team members to help manage operations and keep everything in sync.
- 📝 **Custom Form Builder**
    - Create forms based on your specific requirements to collect client details.
- ⏱️ **Flexible Scheduling Controls**
    - Set time per appointment and define QR code expiry duration.
- 📍 **Live Queue Management**
    - Track clients in real time and manage the queue efficiently with actions like:
        -  Call the next client
        - Skip a client

### 🙋‍♂️ Client
- 📱 **Personal Dashboard**
    - Stay updated with all important queue details in one place.
- 🔢 **Real-Time Queue Position**
    - Know your exact spot in the queue at any moment.
- ⏳ **Estimated Waiting Time**
    - Get a clear idea of how much time is left for your turn.
- 🚨 **Emergency Notifications**
    - Send urgent messages or updates to the admin if needed.
- 🔔 **Custom Reminders**
    - Set alerts so you never miss your turn.
- 🔄 **Spot Exchange**
    - Option to swap your position in the queue with another client.
- ❌ **Easy Cancellation**
    - Cancel your appointment anytime with a single click.


## Contribution
### Forking and Cloning
1) Fork the project.
2) Clone the forked project.
3) Go to the cloned folder and run the following command:
```bash
git remote add upstream https://github.com/original-owner/repo.git
```
### Making changes in code
1) Sync Your Fork **(Important)** - Before starting any work.

- Run the following command:

```bash
git checkout main
git pull upstream main
git push origin main
```
2) Create a new branch
    - Format of branch name: your name in short/label/work in very short format. For example:<br>
    *youraj verma : yv <br>*
    *label: fix/bug/feat/updt <br>*
    *work: readme<br>*
    then branch name will be : `yv/updt/readme`
```bash
git checkout -b yv/updt/readme
```
You are now ready to make changes.

### Pushing your code
1) Make Changes and Commit

```bash
git add .
git commit -m "Describe your changes clearly"
```
2) Keep Your Branch Updated (Recommended)

- Before pushing, run:
```bash
git fetch upstream
git merge upstream/main
```

3) Push Your Changes
```bash
git push origin yv/updt/readme
```
**You can now merge your new branch to the main/dev branch.**
