import React, { useState } from 'react';
import { analyzePortfolio } from '../../Service/PortfolioAnalyze';
import {
    TextField,
    Button,
    Grid,
    Typography,
    Paper,
    Snackbar,
    Alert,
    Card,
    CardContent,
    Divider
} from '@mui/material';

const Portfolio = () => {
    const [items, setItems] = useState([{ symbol: '', quantity: '', price: '' }]);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [snackbarOpen, setSnackbarOpen] = useState(false);

    const handleChange = (index, event) => {
        const values = [...items];
        values[index][event.target.name] = event.target.value;
        setItems(values);
    };

    const handleAddItem = () => {
        setItems([...items, { symbol: '', quantity: '', price: '' }]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        setResult(null);

        const portfolioData = { items };

        try {
            const analysis = await analyzePortfolio(portfolioData);
            setResult(analysis);
        } catch (error) {
            setError(error.message);
            setSnackbarOpen(true);
        }
    };

    const handleCloseSnackbar = () => {
        setSnackbarOpen(false);
    };

    return (
        <Paper style={{ padding: '30px', margin: '20px', fontFamily: 'Arial, sans-serif' }}>
              <h1 className="fw-bold text-center text-danger">Portfolio Analysis</h1>
              <br></br><br></br>
            <form onSubmit={handleSubmit}>
                {items.map((item, index) => (
                    <Grid container spacing={2} key={index}>
                        <Grid item xs={4}>
                            <TextField
                                fullWidth
                                name="symbol"
                                label="Symbol"
                                value={item.symbol}
                                onChange={(event) => handleChange(index, event)}
                                required
                            />
                        </Grid>
                        <Grid item xs={4}>
                            <TextField
                                fullWidth
                                name="quantity"
                                label="Quantity"
                                type="number"
                                value={item.quantity}
                                onChange={(event) => handleChange(index, event)}
                                required
                            />
                        </Grid>
                        <Grid item xs={4}>
                            <TextField
                                fullWidth
                                name="price"
                                label="Price"
                                type="number"
                                value={item.price}
                                onChange={(event) => handleChange(index, event)}
                                required
                            />
                        </Grid>
                    </Grid>
                ))}
                <Grid container spacing={2} style={{ marginTop: '10px' }}>
                    <Grid item>
                        <Button variant="outlined" onClick={handleAddItem}>
                            Add Item
                        </Button>
                    </Grid>
                    <Grid item>
                        <Button variant="contained" color="primary" type="submit">
                            Analyze Portfolio
                        </Button>
                    </Grid>
                </Grid>
            </form>

            {result && (
                <Card style={{ marginTop: '20px', padding: '20px', backgroundColor: '#f9f9f9' }}>
                    <CardContent>
                        <Typography variant="h6" gutterBottom style={{ fontWeight: 'bold' }}>
                            Analysis Result
                        </Typography>
                        <Divider style={{ margin: '10px 0' }} />
                        <Typography variant="subtitle1" style={{ fontWeight: 'bold' }}>
                            Total Value: ₹{result.total_value}
                        </Typography>
                        <Typography variant="subtitle1" style={{ fontWeight: 'bold' }}>
                            Items Added: {result.total_items}
                        </Typography>

                        <Typography variant="h6" gutterBottom style={{ fontWeight: 'bold', marginTop: '20px' }}>
                            Risk Analysis
                        </Typography>
                        <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'Open Sans,Arial ,sans-serif', fontSize:'16px' }}>
                            {result.risk_analysis}
                        </pre>

                        <Divider style={{ margin: '20px 0' }} />
                    </CardContent>
                </Card>
            )}

            <Snackbar
                open={snackbarOpen}
                autoHideDuration={6000}
                onClose={handleCloseSnackbar}
            >
                <Alert onClose={handleCloseSnackbar} severity="error">
                    {error}
                </Alert>
            </Snackbar>
        </Paper>
    );
};

export default Portfolio;
