const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

let reviewsPath = fs.existsSync(path.join(__dirname, 'reviews.json'))
  ? path.join(__dirname, 'reviews.json')
  : path.join(__dirname, 'data', 'reviews.json');

let dealershipsPath = fs.existsSync(path.join(__dirname, 'dealerships.json'))
  ? path.join(__dirname, 'dealerships.json')
  : path.join(__dirname, 'data', 'dealerships.json');

const reviews_data = JSON.parse(fs.readFileSync(reviewsPath, 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync(dealershipsPath, 'utf8'));

let inMemoryReviews = [...reviews_data['reviews']];
let inMemoryDealerships = [...dealerships_data['dealerships']];

let mongoConnected = false;
const Reviews = require('./review');
const Dealerships = require('./dealership');

mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' })
  .then(() => {
    mongoConnected = true;
    console.log("Connected to MongoDB successfully");
    Reviews.deleteMany({}).then(() => {
      Reviews.insertMany(reviews_data['reviews']);
    });
    Dealerships.deleteMany({}).then(() => {
      Dealerships.insertMany(dealerships_data['dealerships']);
    });
  })
  .catch((err) => {
    mongoConnected = false;
    console.log("MongoDB connection failed, falling back to in-memory JSON data:", err.message);
  });

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    if (mongoConnected) {
      const documents = await Reviews.find();
      return res.json(documents);
    }
    res.json(inMemoryReviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    if (mongoConnected) {
      const documents = await Reviews.find({ dealership: dealerId });
      return res.json(documents);
    }
    const filtered = inMemoryReviews.filter((r) => r.dealership === dealerId || r.dealership === req.params.id);
    res.json(filtered);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    if (mongoConnected) {
      const documents = await Dealerships.find();
      return res.json(documents);
    }
    res.json(inMemoryDealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    if (mongoConnected) {
      const documents = await Dealerships.find({
        state: { $regex: new RegExp(`^${state}$`, 'i') }
      });
      return res.json(documents);
    }
    const filtered = inMemoryDealerships.filter(
      (d) => d.state.toLowerCase() === state.toLowerCase()
    );
    res.json(filtered);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    if (mongoConnected) {
      const documents = await Dealerships.find({ id: dealerId });
      return res.json(documents);
    }
    const filtered = inMemoryDealerships.filter((d) => d.id === dealerId);
    res.json(filtered);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    const data = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    let new_id = 1;
    if (mongoConnected) {
      const documents = await Reviews.find().sort({ id: -1 });
      if (documents.length > 0) {
        new_id = documents[0]['id'] + 1;
      }
      const review = new Reviews({
        "id": new_id,
        "name": data['name'],
        "dealership": data['dealership'],
        "review": data['review'],
        "purchase": data['purchase'],
        "purchase_date": data['purchase_date'],
        "car_make": data['car_make'],
        "car_model": data['car_model'],
        "car_year": data['car_year'],
      });
      const savedReview = await review.save();
      return res.json(savedReview);
    }

    if (inMemoryReviews.length > 0) {
      const sorted = [...inMemoryReviews].sort((a, b) => b.id - a.id);
      new_id = sorted[0].id + 1;
    }
    const newReview = {
      id: new_id,
      name: data['name'],
      dealership: parseInt(data['dealership']),
      review: data['review'],
      purchase: data['purchase'],
      purchase_date: data['purchase_date'],
      car_make: data['car_make'],
      car_model: data['car_model'],
      car_year: data['car_year'],
    };
    inMemoryReviews.push(newReview);
    res.json(newReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
