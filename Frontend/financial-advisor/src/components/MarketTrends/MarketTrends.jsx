import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Tab,
  Tabs,
  Card,
  CardHeader,
  CardContent,
  CircularProgress,
  Alert,
  Grid
} from '@mui/material';
import { fetchMarketData } from '../../Service/marketTrendsService'; 

const MarketTrends = () => {
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('gainers');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchMarketData();
        setMarketData(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const formatChange = (percent_change) => {
    return (
      <Typography style={{ color: percent_change > 0 ? 'green' : 'red' }}>
        {percent_change > 0 ? '▲' : '▼'} {percent_change}%
      </Typography>
    );
  };

  if (loading) return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh' 
    }}>
      <CircularProgress />
    </div>
  );
  
  if (error) return <Alert severity="error">Error: {error}</Alert>;

  return (
    <Container>
      <Typography variant="h4" align="center" style={{ margin: '2rem 0', fontWeight: 600, color: '#343a40' }}>
        Market Trends
      </Typography>
      <Tabs value={activeTab} onChange={(event, newValue) => setActiveTab(newValue)} centered>
        <Tab label="Top Gainers" value="gainers" />
        <Tab label="Top Losers" value="losers" />
      </Tabs>

      <Grid container spacing={4} style={{ marginTop: '1rem' }}>
        {activeTab === 'gainers' ? (
          marketData.top_gainers.map((stock) => (
            <Grid item key={stock.ticker_id} xs={12} sm={6} md={4}>
              <Card style={{ borderRadius: '10px' }}>
                <CardHeader 
                  title={stock.company_name} 
                  style={{ 
                    backgroundColor: '#28a745', 
                    color: 'white', 
                    fontSize: '1rem', // Reduced font size
                    padding: '8px 16px' // Adjusted padding for simplicity
                  }} 
                />
                <CardContent>
                  <Typography variant="body1"><strong>Price:</strong> ₹{isNaN(stock.price) ? 'N/A' : Number(stock.price).toFixed(2)}</Typography>
                  <Typography variant="body1"><strong>Change:</strong> {formatChange(stock.percent_change)}</Typography>
                  <Typography variant="body1"><strong>Volume:</strong> {stock.volume.toLocaleString()}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          marketData.top_losers.map((stock) => (
            <Grid item key={stock.ticker_id} xs={12} sm={6} md={4}>
              <Card style={{ borderRadius: '10px' }}>
                <CardHeader 
                  title={stock.company_name} 
                  style={{ 
                    backgroundColor: '#dc3545', 
                    color: 'white', 
                    fontSize: '1rem', // Reduced font size
                    padding: '8px 16px' // Adjusted padding for simplicity
                  }} 
                />
                <CardContent>
                  <Typography variant="body1"><strong>Price:</strong> ₹{isNaN(stock.price) ? 'N/A' : Number(stock.price).toFixed(2)}</Typography>
                  <Typography variant="body1"><strong>Change:</strong> {formatChange(stock.percent_change)}</Typography>
                  <Typography variant="body1"><strong>Volume:</strong> {stock.volume.toLocaleString()}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
    </Container>
  );
};

export default MarketTrends;
