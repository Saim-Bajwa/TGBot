const express = require('express');
const app = express();
const admin = require('firebase-admin');

// Initialize Firebase Admin SDK (you need to set this up with your Firebase project)
admin.initializeApp({
  credential: admin.credential.applicationDefault(),
  databaseURL: 'https://tg-bot-user-default-rtdb.asia-southeast1.firebasedatabase.app'
});
const db = admin.database();

app.get('/reward', async (req, res) => {
  const userId = req.query.userid;
  if (!userId) {
    return res.status(400).send('Missing userid');
  }

  try {
    const userRef = db.ref(`users/${userId}`);
    const snapshot = await userRef.once('value');
    let userData = snapshot.val();

    if (!userData) {
      return res.status(404).send('User not found');
    }

    // Add reward, e.g., +500 balance
    userData.balance = (userData.balance || 0) + 500;

    // Update in database
    await userRef.set(userData);

    console.log(`Rewarded user ${userId} with +500 balance`);

    res.status(200).send('Reward processed');
  } catch (error) {
    console.error('Error processing reward:', error);
    res.status(500).send('Server error');
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
