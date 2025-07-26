import React, { useState, useEffect } from 'react';
import './Community.css';

const Community = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [userBalance, setUserBalance] = useState({ balance: 0, level: 1, experience_points: 0 });
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchCommunityData();
  }, []);

  const fetchCommunityData = async () => {
    try {
      setLoading(true);
      
      // Récupérer le token d'authentification
      const token = localStorage.getItem('token');
      if (!token) {
        console.warn('No auth token found');
        return;
      }

      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      // Récupérer le solde de l'utilisateur
      try {
        const balanceResponse = await fetch(`${backendUrl}/api/currency/balance`, { headers });
        if (balanceResponse.ok) {
          const balanceData = await balanceResponse.json();
          setUserBalance(balanceData);
        }
      } catch (error) {
        console.error('Error fetching balance:', error);
      }

      // Récupérer les statistiques générales
      try {
        const statsResponse = await fetch(`${backendUrl}/api/community/stats`, { headers });
        if (statsResponse.ok) {
          const statsData = await statsResponse.json();
          setStats(statsData);
        }
      } catch (error) {
        console.error('Error fetching stats:', error);
      }

    } catch (error) {
      console.error('Error fetching community data:', error);
    } finally {
      setLoading(false);
    }
  };

  const claimDailyBonus = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${backendUrl}/api/currency/daily-bonus`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      
      if (response.ok) {
        alert(`Bonus réclamé ! +${data.bonus_amount} coins`);
        setUserBalance(prev => ({ 
          ...prev, 
          balance: data.new_balance 
        }));
      } else {
        alert(data.detail || 'Erreur lors de la réclamation du bonus');
      }
    } catch (error) {
      console.error('Error claiming daily bonus:', error);
      alert('Erreur de connexion');
    }
  };

  if (loading) {
    return (
      <div className="community-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Chargement de la communauté...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="community-container">
      <header className="community-header">
        <h1>🎮 Espace Communauté Oupafamilly</h1>
        <div className="user-stats">
          <div className="stat-card">
            <span className="stat-value">{userBalance.balance}</span>
            <span className="stat-label">💰 Coins</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">Niv. {userBalance.level}</span>
            <span className="stat-label">⬆️ Niveau</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{userBalance.experience_points}</span>
            <span className="stat-label">⭐ XP</span>
          </div>
          <button className="daily-bonus-btn" onClick={claimDailyBonus}>
            🎁 Bonus Quotidien
          </button>
        </div>
      </header>

      <nav className="community-nav">
        <button 
          className={activeTab === 'overview' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('overview')}
        >
          📊 Vue d'ensemble
        </button>
        <button 
          className={activeTab === 'marketplace' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('marketplace')}
        >
          🛒 Marketplace
        </button>
        <button 
          className={activeTab === 'chat' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('chat')}
        >
          💬 Chat
        </button>
        <button 
          className={activeTab === 'activity' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('activity')}
        >
          📰 Activités
        </button>
        <button 
          className={activeTab === 'betting' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('betting')}
        >
          🎲 Paris
        </button>
        <button 
          className={activeTab === 'leaderboards' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setActiveTab('leaderboards')}
        >
          🏆 Classements
        </button>
      </nav>

      <main className="community-content">
        {activeTab === 'overview' && <OverviewTab stats={stats} />}
        {activeTab === 'marketplace' && <MarketplaceTab />}
        {activeTab === 'chat' && <ChatTab />}
        {activeTab === 'activity' && <ActivityTab />}
        {activeTab === 'betting' && <BettingTab />}
        {activeTab === 'leaderboards' && <LeaderboardsTab />}
      </main>
    </div>
  );
};

// Composant Vue d'ensemble
const OverviewTab = ({ stats }) => (
  <div className="overview-tab">
    <div className="stats-grid">
      <div className="stat-box">
        <h3>👥 Membres Total</h3>
        <p className="big-number">{stats.total_members || 0}</p>
      </div>
      <div className="stat-box">
        <h3>🏆 Équipes Actives</h3>
        <p className="big-number">{stats.total_teams || 0}</p>
      </div>
      <div className="stat-box">
        <h3>🎯 Tournois</h3>
        <p className="big-number">{stats.total_tournaments || 0}</p>
      </div>
      <div className="stat-box">
        <h3>💰 Coins en Circulation</h3>
        <p className="big-number">{stats.total_coins_circulation || 0}</p>
      </div>
    </div>

    <div className="recent-activity">
      <h3>🔥 Activité Récente</h3>
      <div className="activity-list">
        {stats.recent_activities && stats.recent_activities.length > 0 ? (
          stats.recent_activities.map((activity, index) => (
            <div key={index} className="activity-item">
              <span className="activity-icon">📢</span>
              <span className="activity-text">{activity.description || 'Activité de la communauté'}</span>
              <span className="activity-time">{new Date(activity.created_at).toLocaleTimeString()}</span>
            </div>
          ))
        ) : (
          <p className="no-data">Aucune activité récente</p>
        )}
      </div>
    </div>
  </div>
);

// Composant Marketplace
const MarketplaceTab = () => {
  const [items, setItems] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);

  const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchMarketplaceData();
  }, []);

  const fetchMarketplaceData = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      // Récupérer les articles marketplace
      const itemsResponse = await fetch(`${backendUrl}/api/currency/marketplace`, { headers });
      if (itemsResponse.ok) {
        const itemsData = await itemsResponse.json();
        setItems(itemsData);
      }

      // Récupérer l'inventaire
      const inventoryResponse = await fetch(`${backendUrl}/api/currency/inventory`, { headers });
      if (inventoryResponse.ok) {
        const inventoryData = await inventoryResponse.json();
        setInventory(inventoryData);
      }

    } catch (error) {
      console.error('Error fetching marketplace data:', error);
    } finally {
      setLoading(false);
    }
  };

  const buyItem = async (itemId, itemName, price) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${backendUrl}/api/currency/marketplace/buy/${itemId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();

      if (response.ok) {
        alert(`Achat réussi ! Vous avez acheté ${itemName} pour ${price} coins`);
        fetchMarketplaceData(); // Recharger les données
      } else {
        alert(data.detail || 'Erreur lors de l\'achat');
      }
    } catch (error) {
      console.error('Error buying item:', error);
      alert('Erreur de connexion');
    }
  };

  if (loading) return <div className="loading">Chargement de la marketplace...</div>;

  return (
    <div className="marketplace-tab">
      <div className="marketplace-section">
        <h3>🛒 Articles Disponibles</h3>
        <div className="items-grid">
          {items.map(item => (
            <div key={item.id} className="item-card">
              <div className="item-header">
                <span className="item-type">{getItemTypeIcon(item.item_type)}</span>
                <h4>{item.name}</h4>
                {item.is_premium && <span className="premium-badge">⭐ Premium</span>}
              </div>
              <p className="item-description">{item.description}</p>
              <div className="item-footer">
                <span className="item-price">💰 {item.price} coins</span>
                <button 
                  className="buy-btn"
                  onClick={() => buyItem(item.id, item.name, item.price)}
                  disabled={inventory.some(inv => inv.item_id === item.id)}
                >
                  {inventory.some(inv => inv.item_id === item.id) ? 'Possédé' : 'Acheter'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="inventory-section">
        <h3>🎒 Mon Inventaire</h3>
        <div className="inventory-grid">
          {inventory.length > 0 ? (
            inventory.map(item => (
              <div key={item.id} className="inventory-item">
                <span className="item-icon">{getItemTypeIcon(item.item_type)}</span>
                <span className="item-name">{item.item_name}</span>
                <span className="purchase-date">
                  Acheté le {new Date(item.purchased_at).toLocaleDateString()}
                </span>
              </div>
            ))
          ) : (
            <p className="no-data">Votre inventaire est vide</p>
          )}
        </div>
      </div>
    </div>
  );
};

// Composant Chat (version simple pour demo)
const ChatTab = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [selectedChannel, setSelectedChannel] = useState('general');

  const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchMessages();
  }, [selectedChannel]);

  const fetchMessages = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${backendUrl}/api/chat/messages/${selectedChannel}?limit=20`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(data);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${backendUrl}/api/chat/messages`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          channel: selectedChannel,
          content: newMessage,
          message_type: 'text'
        })
      });

      if (response.ok) {
        setNewMessage('');
        fetchMessages(); // Recharger les messages
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const channels = ['general', 'cs2', 'lol', 'wow', 'sc2', 'minecraft'];

  return (
    <div className="chat-tab">
      <div className="chat-channels">
        {channels.map(channel => (
          <button
            key={channel}
            className={selectedChannel === channel ? 'channel-btn active' : 'channel-btn'}
            onClick={() => setSelectedChannel(channel)}
          >
            #{channel}
          </button>
        ))}
      </div>

      <div className="chat-messages">
        {messages.map(message => (
          <div key={message.id} className="message">
            <span className="message-author">{message.author_name}:</span>
            <span className="message-content">{message.content}</span>
            <span className="message-time">
              {new Date(message.created_at).toLocaleTimeString()}
            </span>
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder={`Message #${selectedChannel}...`}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Envoyer</button>
      </div>
    </div>
  );
};

// Autres composants de base
const ActivityTab = () => <div className="tab-content">🚧 Feed d'Activité - En cours de développement</div>;
const BettingTab = () => <div className="tab-content">🚧 Système de Paris - En cours de développement</div>;
const LeaderboardsTab = () => <div className="tab-content">🚧 Classements - En cours de développement</div>;

// Fonction utilitaire pour les icônes
const getItemTypeIcon = (type) => {
  const icons = {
    avatar: '🎭',
    badge: '🏷️',
    title: '👑',
    banner: '🖼️',
    emote: '😀'
  };
  return icons[type] || '🛒';
};

export default Community;