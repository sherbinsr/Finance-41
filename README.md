# Finance-41

Finance-41 is a financial advisor application that leverages GenAI technology to provide users with personalized insights and analytics for informed investment decisions. The application is built using React for the frontend and FastAPI for the backend, focusing on user-friendly design and robust functionality. By utilizing the Grok API with a fine-tuned model, users can receive tailored financial advice to enhance their investment strategies.

## Features
- **User Authentication:** Secure login and registration with Google SSO integration.
- **Get Financial Advice from Chatbot:** Interact with a chatbot to receive personalized financial advice.
- **Batch Jobs:** Automated process that sends users the top gainers every day at 11:00 AM to keep them informed of the best-performing stocks.
- **Market Trends:** Fetchs and displays the realtime latest market trends.Which includes top gainers and top  losers
 - **Market News:** Stay updated with the latest financial news, with options to sort and filter news articles by latest news.
- **Industrial Search:** A comprehensive search feature that allows users to explore various industries and sectors for better investment insights.
- **Quick Contact Form:** Easily reach out for support or inquiries using a quick contact form integrated with EmailJS.
- **User Analytics:** Track user activity and display analytics.
- **Responsive Design:** Mobile-friendly layout for accessibility on various devices.
- **Performance Optimization:** Efficient data handling and rendering for a seamless user experience.

## Tech Stack

- **Frontend:** React, Bootstrap
- **Backend:** FastAPI
- **Database:** Sqlite
- **Deployment:** Docker

## Installation

### Prerequisites

- Python 3.x
- Node.js
- Sqlite

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sherbinsr/Finance-41.git
   cd Finance-41
   ```
 2. Navigate to the backend directory:
    ```bash
    cd backend
    ```
3. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the database:
    - Create a Sqlite database and configure your database settings.
5. Run the FastAPI server:
    ```bash
     uvicorn app.main:app --reload
    ```
### Frontend Setup

1. Navigate to the frontend directory:
    ```bash
    cd frontend/financial-advisor
    ```
2. Install required packages:
    ```bash
    npm install
    ```
3. Run the React application:
    ```bash
    npm start
    ```
### usage
- Access the React application at http://localhost:3000.
- Access the Fastapi application at http://127.0.0.1:8000/

## Conclusion

Finance-41 aims to empower users with the tools and insights necessary for effective financial decision-making. By leveraging modern web technologies and a user-centric design, the application seeks to provide a seamless experience for individuals looking to navigate the complexities of investing. We welcome feedback and contributions to enhance the platform further. Join us on this journey to make financial knowledge accessible and actionable for everyone!

Feel free to customize sections, add more details, or remove parts as needed!
