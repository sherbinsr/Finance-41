import React, { useState } from 'react';
import axios from 'axios';
import {
    TextField,
    Button,
    Typography,
    Paper,
    Divider,
    Card,
    CardContent,
    CardMedia,
    Grid
} from '@mui/material';

const StockInfo = () => {
    const [stockName, setStockName] = useState('');
    const [stockData, setStockData] = useState(null);
    const [error, setError] = useState('');

    const handleInputChange = (event) => {
        setStockName(event.target.value);
    };

    const fetchStockInfo = async () => {
        setError('');
        setStockData(null);
        try {
            const response = await axios.get(`https://finance-41-1081098542602.us-central1.run.app/proxy/8000/stock`, {
                params: { name: stockName },
            });
            setStockData(response.data);
        } catch (err) {
            setError('Error fetching stock data. Please try again.');
        }
    };

    return (
        <Paper style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
            <Typography variant="h5" gutterBottom>
                Stock Information
            </Typography>
            <TextField
                label="Enter Stock Name"
                variant="outlined"
                fullWidth
                value={stockName}
                onChange={handleInputChange}
                style={{ marginBottom: '10px' }}
            />
            <br></br>
            <Button variant="contained" color="primary" onClick={fetchStockInfo}>
                Get Stock Info
            </Button>

            {error && <Typography color="error">{error}</Typography>}

            {stockData && (
                <div style={{ marginTop: '20px' }}>
                    <Card variant="outlined" style={{ marginBottom: '20px' }}>
                        <CardContent>
                            <Typography variant="body1">
                                <strong>Company Name:</strong> {stockData.companyName || 'N/A'}
                            </Typography>
                            <Typography variant="body1">
                                <strong>Industry:</strong> {stockData.industry || 'N/A'}
                            </Typography>
                            <Typography variant="body1">
                                <strong>Description:</strong> {stockData.companyProfile?.companyDescription || 'N/A'}
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid item xs={6}>
                                    <Typography variant="body1">
                                        <strong>Current Price (BSE):</strong> ₹{stockData.currentPrice?.BSE || 'N/A'}
                                    </Typography>
                                </Grid>
                                <Grid item xs={6}>
                                    <Typography variant="body1">
                                        <strong>Current Price (NSE):</strong> ₹{stockData.currentPrice?.NSE || 'N/A'}
                                    </Typography>
                                </Grid>
                            </Grid>
                            <Typography variant="body1">
                                <strong>Percent Change:</strong> {stockData.percentChange || 'N/A'}
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid item xs={6}>
                                    <Typography variant="body1">
                                        <strong>Year High:</strong> ₹{stockData.yearHigh || 'N/A'}
                                    </Typography>
                                </Grid>
                                <Grid item xs={6}>
                                    <Typography variant="body1">
                                        <strong>Year Low:</strong> ₹{stockData.yearLow || 'N/A'}
                                    </Typography>
                                </Grid>
                            </Grid>
                            <Typography variant="body1">
                                <strong>Risk Meter:</strong> {stockData.riskMeter?.categoryName || 'N/A'}
                            </Typography>
                        </CardContent>
                    </Card>

                    <Divider style={{ margin: '20px 0' }} />

                    <Card variant="outlined">
                        <CardContent>
                            <Typography variant="h6">Recent News:</Typography>
                            {stockData.recentNews && stockData.recentNews.length > 0 ? (
                                stockData.recentNews.map((news) => (
                                    <Card key={news.id} style={{ marginBottom: '10px' }}>
                                        <CardMedia
                                            component="img"
                                            height="140"
                                            image={news.thumbnailimage}
                                            alt={news.headline}
                                        />
                                        <CardContent>
                                            <Typography variant="body1">{news.headline}</Typography>
                                            <Typography variant="body2" color="textSecondary">
                                                <a href={news.url} target="_blank" rel="noopener noreferrer">
                                                    Read more
                                                </a>
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                ))
                            ) : (
                                <Typography variant="body1">No recent news available.</Typography>
                            )}
                        </CardContent>
                    </Card>
                </div>
            )}
        </Paper>
    );
};

export default StockInfo;
