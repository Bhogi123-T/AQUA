import React, { useState, useEffect } from 'react';
import { useTranslation } from '../context/TranslationContext';
import { motion } from 'framer-motion';
import { Activity, ShieldCheck, Cpu, Globe, ArrowRight } from 'lucide-react';

const Home = () => {
    const { t } = useTranslation();
    const [stats, setStats] = useState({
        weather: "28°C Clear",
        market_trend: "+4.2% Today",
        active_experts: 18,
        global_users: "8.4k+"
    });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await fetch('/api/landing');
                const data = await response.json();
                if (data.status === 'success') {
                    setStats(data.live_stats);
                }
            } catch (error) {
                console.error("Failed to fetch landing stats:", error);
            }
        };
        fetchStats();
    }, []);

    const features = [
        { icon: <Activity className="text-primary" size={40} />, title: t('feat_disease_title'), desc: t('feat_disease_desc'), link: '/farmer/disease' },
        { icon: <ShieldCheck className="text-secondary" size={40} />, title: t('feat_yield_title'), desc: t('feat_yield_desc'), link: '/farmer/yield' },
        { icon: <Cpu className="text-accent" size={40} />, title: t('feat_loc_title'), desc: t('feat_loc_desc'), link: '/farmer/location' },
        { icon: <Globe className="text-violet" size={40} />, title: t('feat_market_title'), desc: t('feat_market_desc'), link: '/market' }
    ];

    return (
        <div className="home-page">
            {/* Hero Section */}
            <section className="hero-section">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <h1 dangerouslySetInnerHTML={{ __html: t('hero_title').replace('\n', '<br/>') }}></h1>
                    <p className="hero-description">{t('hero_subtitle')}</p>

                    <div className="hero-actions">
                        <a href="/signup" className="app-btn-large shimmer-btn">
                            {t('get_started')} <ArrowRight size={20} />
                        </a>
                    </div>
                </motion.div>

                {/* Animated Stats Bar */}
                <div className="stats-grid">
                    <div className="stat-card">
                        <div className="stat-label">{t('live_weather')}</div>
                        <div className="stat-value">{stats.weather}</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-label">{t('market_trend')}</div>
                        <div className="stat-value">{stats.market_trend}</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-label">{t('active_experts')}</div>
                        <div className="stat-value">{stats.active_experts}</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-label">Global Users</div>
                        <div className="stat-value">{stats.global_users}</div>
                    </div>
                </div>
            </section>

            {/* Features Grid */}
            <section className="features-section">
                <div className="section-header">
                    <h2>{t('feature_title')}</h2>
                    <p>{t('feature_subtitle')}</p>
                </div>

                <div className="grid">
                    {features.map((feat, idx) => (
                        <motion.a
                            key={idx}
                            href={feat.link}
                            className="app-card"
                            whileHover={{ y: -10 }}
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                        >
                            <div className="app-emoji">{feat.icon}</div>
                            <h3>{feat.title}</h3>
                            <p>{feat.desc}</p>
                        </motion.a>
                    ))}
                </div>
            </section>

            {/* AI Call to Action */}
            <section className="ai-cta">
                <div className="app-card glass-card">
                    <h2>{t('cta_title')}</h2>
                    <p>{t('cta_desc')}</p>
                    <div className="cta-actions">
                        <a href="/login" className="app-btn-large active-btn">{t('cta_login_now')}</a>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;
