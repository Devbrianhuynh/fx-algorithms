API_KEY = 'eec6ddcc5fa2bc2115c3a9ae1069c5da-183f9c7dcc76b62a9a77824419b8538a'
ACCOUNT_ID = '101-001-28743255-001'
OANDA_URL = 'https://api-fxpractice.oanda.com/v3'
STREAM_URL = 'https://stream-fxpractice.oanda.com/v3'
SECURE_HEADER = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
BUY = 1
SELL = -1
NONE = 0
MONGO_CONNECTION_STR = 'mongodb+srv://Admin:administratormongodb@cluster0.zuchy7y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'