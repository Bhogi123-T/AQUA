import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'
import { TranslationProvider } from './context/TranslationContext.jsx'
import { AuthProvider } from './context/AuthContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <BrowserRouter>
            <AuthProvider>
                <TranslationProvider>
                    <App />
                </TranslationProvider>
            </AuthProvider>
        </BrowserRouter>
    </React.StrictMode>,
)

// Initialize Twemoji globally after render
window.onload = () => {
    if (window.twemoji) {
        window.twemoji.parse(document.body, {
            folder: 'svg',
            ext: '.svg'
        });
    }
};
