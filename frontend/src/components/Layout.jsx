import { useTranslation } from '../context/TranslationContext';
import { useAuth } from '../context/AuthContext';
import { Menu, X, Globe, LogIn, UserPlus, Info, Phone, LogOut, Settings, HelpCircle, LayoutDashboard, ShoppingCart, Activity, MapPin, Database, Droplets, User } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Layout = ({ children }) => {
    const { t, lang, changeLang } = useTranslation();
    const { user, logout, loading } = useAuth();
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [isOnline, setIsOnline] = useState(navigator.onLine);
    const [scrolled, setScrolled] = useState(false);

    // ... useEffects ...
    useEffect(() => {
        if (sidebarOpen) {
            document.body.classList.add('sidebar-open');
        } else {
            document.body.classList.remove('sidebar-open');
        }
    }, [sidebarOpen]);

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth > 1024) setSidebarOpen(false);
        };
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        const handleStatusChange = () => setIsOnline(navigator.onLine);

        window.addEventListener('resize', handleResize);
        window.addEventListener('scroll', handleScroll);
        window.addEventListener('online', handleStatusChange);
        window.addEventListener('offline', handleStatusChange);

        return () => {
            window.removeEventListener('resize', handleResize);
            window.removeEventListener('scroll', handleScroll);
            window.removeEventListener('online', handleStatusChange);
            window.removeEventListener('offline', handleStatusChange);
        };
    }, []);

    const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

    const languages = [
        { code: 'en', label: 'English', flag: '🇺🇸' },
        { code: 'te', label: 'తెలుగు', flag: '🇮🇳' },
        { code: 'hi', label: 'हिन्दी', flag: '🇮🇳' },
        { code: 'vi', label: 'Tiếng Việt', flag: '🇻🇳' },
        { code: 'no', label: 'Norsk', flag: '🇳🇴' }
    ];

    return (
        <div className={`app-container ${sidebarOpen ? 'sidebar-open' : ''}`}>
            {/* Live Ticker */}
            <div className="live-ticker">
                <div className="ticker-content">
                    <span className="live-pulse"></span>
                    {t('live_market_ticker')} • {t('ticker_prices_updated')} • {t('ticker_expert_online')} • {t('ticker_global_demand')}
                </div>
            </div>

            {/* Navbar */}
            <nav className={scrolled ? 'scrolled' : ''}>
                <div className="nav-brand">
                    <button id="hamburger" onClick={toggleSidebar} aria-label="Toggle Menu">
                        <div className="ham-inner">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </button>
                    <a href="/" className="logo">AQUASPHERE AI</a>
                </div>

                <div className="nav-actions">
                    <div id="connection-badge" className={isOnline ? 'online' : 'offline'}>
                        <Activity size={16} />
                        <span id="connection-text">{isOnline ? t('status_online') : t('status_offline')}</span>
                    </div>

                    <div className="lang-switcher-container">
                        <select
                            className="lang-select"
                            value={lang}
                            onChange={(e) => changeLang(e.target.value)}
                        >
                            {languages.map(l => (
                                <option key={l.code} value={l.code}>{l.flag} {l.label}</option>
                            ))}
                        </select>
                    </div>

                    <div className="nav-links">
                        {user ? (
                            <div className="user-profile-nav">
                                <div className="user-info-brief">
                                    <span className="user-role-tag">{user.role}</span>
                                    <span className="user-name">{user.name}</span>
                                </div>
                                <button onClick={logout} className="logout-icon-btn" title="Logout">
                                    <LogOut size={18} />
                                </button>
                            </div>
                        ) : (
                            <a href="/login" className="app-btn-large">
                                <LogIn size={18} />
                                <span>{t('login')}</span>
                            </a>
                        )}
                    </div>
                </div>
            </nav>

            {/* Sidebar Overlay */}
            <AnimatePresence>
                {sidebarOpen && (
                    <motion.div
                        className="sidebar-overlay"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setSidebarOpen(false)}
                    />
                )}
            </AnimatePresence>

            {/* Sidebar */}
            <aside id="sidebar" className={sidebarOpen ? 'open' : ''}>
                <div className="sidebar-content">
                    <div className="nav-category">{t('nav_category_tools')}</div>

                    {user ? (
                        <a href="/dashboard" className="nav-item">
                            <LayoutDashboard size={20} className="emo" />
                            <span>{t('nav_dashboard')}</span>
                        </a>
                    ) : (
                        <a href="/home" className="nav-item">
                            <LayoutDashboard size={20} className="emo" />
                            <span>{t('nav_home')}</span>
                        </a>
                    )}

                    <a href="/market" className="nav-item">
                        <Activity size={20} className="emo" />
                        <span>{t('nav_market')}</span>
                    </a>
                    <a href="/farmer/disease" className="nav-item">
                        <Droplets size={20} className="emo" />
                        <span>{t('nav_disease')}</span>
                    </a>

                    {user && (
                        <>
                            <div className="nav-category">AQUACYCLE</div>
                            <a href="/aquacycle/network" className="nav-item">
                                <Users size={20} className="emo" />
                                <span>Network</span>
                            </a>
                            <a href="/aquacycle/trade" className="nav-item">
                                <ShoppingCart size={20} className="emo" />
                                <span>Trade Link</span>
                            </a>
                        </>
                    )}

                    <div className="nav-category">{t('nav_category_account')}</div>
                    {user ? (
                        <>
                            <a href="/profile" className="nav-item">
                                <User size={20} className="emo" />
                                <span>Profile</span>
                            </a>
                            <a href="#" onClick={logout} className="nav-item logout-item">
                                <LogOut size={20} className="emo" />
                                <span>{t('logout')}</span>
                            </a>
                        </>
                    ) : (
                        <>
                            <a href="/login" className="nav-item">
                                <LogIn size={20} className="emo" />
                                <span>{t('login')}</span>
                            </a>
                            <a href="/register-role" className="nav-item">
                                <UserPlus size={20} className="emo" />
                                <span>{t('signup')}</span>
                            </a>
                        </>
                    )}

                    <div className="sidebar-footer">
                        <div className="created-by">Created by <strong>Bhogi</strong></div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="container">
                {children}
            </main>

            {/* Footer */}
            <footer className="glass-footer">
                <div className="footer-content">
                    <div className="footer-logo">AQUASPHERE AI</div>
                    <p>{t('footer_vision')}</p>
                    <div className="footer-credits">
                        © 2026 AquaSphere AI • {t('created_by')} <strong>Bhogi</strong>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
