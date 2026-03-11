import React, { createContext, useState, useContext, useEffect } from 'react';

const TranslationContext = createContext();

export const TranslationProvider = ({ children }) => {
    const [translations, setTranslations] = useState({});
    const [lang, setLang] = useState('en');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTranslations = async () => {
            try {
                const response = await fetch('/api/translations');
                const data = await response.json();
                setTranslations(data);

                // Try to get saved language from localStorage
                const savedLang = localStorage.getItem('aqua_lang') || 'en';
                setLang(savedLang);
            } catch (error) {
                console.error("Failed to fetch translations:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchTranslations();
    }, []);

    const changeLang = (newLang) => {
        setLang(newLang);
        localStorage.setItem('aqua_lang', newLang);
        // Dispatch event for components that might need it
        window.dispatchEvent(new Event('languageChange'));
    };

    const t = (key) => {
        return translations[lang]?.[key] || translations['en']?.[key] || key;
    };

    return (
        <TranslationContext.Provider value={{ t, lang, changeLang, loading, translations }}>
            {!loading && children}
        </TranslationContext.Provider>
    );
};

export const useTranslation = () => useContext(TranslationContext);
