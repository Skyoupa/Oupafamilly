import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Inventaire.css';

const Inventaire = ({ isOpen, onClose }) => {
  const { API_BASE_URL, user } = useAuth();
  const [inventory, setInventory] = useState({
    avatar: [],
    banner: [],
    badge: [],
    custom_tag: [],
    title: [],
    theme: [],
    emote: []
  });
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('banner');

  useEffect(() => {
    if (isOpen) {
      fetchInventory();
    }
  }, [isOpen]);

  const fetchInventory = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/currency/inventory`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setInventory(data);
      }
    } catch (error) {
      console.error('Erreur chargement inventaire:', error);
    } finally {
      setLoading(false);
    }
  };

  const equipItem = async (inventoryItemId) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/currency/inventory/equip/${inventoryItemId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message);
        fetchInventory(); // Recharger l'inventaire
      } else {
        const error = await response.json();
        alert(error.detail || 'Erreur lors de l\'équipement');
      }
    } catch (error) {
      console.error('Erreur équipement:', error);
      alert('Erreur lors de l\'équipement');
    }
  };

  const getItemPreview = (item) => {
    const itemType = item.item_type;
    const itemData = item.item_data || {};

    switch (itemType) {
      case 'banner':
        return (
          <div className="banner-preview">
            <div className="banner-icon">🖼️</div>
            <span>Bannière</span>
          </div>
        );
      case 'avatar':
        return (
          <div className="avatar-preview">
            <div className="avatar-icon">👤</div>
            <span>Avatar</span>
          </div>
        );
      case 'badge':
        return (
          <div className="badge-preview">
            <div className="badge-icon">🏆</div>
            <span>{itemData.text || 'Badge'}</span>
          </div>
        );
      case 'custom_tag':
        return (
          <div 
            className="tag-preview"
            style={{
              background: itemData.background || 'linear-gradient(135deg, #667eea, #764ba2)',
              color: itemData.text_color || '#ffffff'
            }}
          >
            MEMBRE
          </div>
        );
      case 'title':
        return (
          <div className="title-preview">
            <div className="title-icon">👑</div>
            <span style={{ color: itemData.title_color || '#6c5ce7' }}>
              {itemData.title_text || 'Titre'}
            </span>
          </div>
        );
      case 'theme':
        return (
          <div className="theme-preview">
            <div className="theme-icon">🎨</div>
            <span>Thème</span>
          </div>
        );
      default:
        return (
          <div className="default-preview">
            <div className="default-icon">📦</div>
            <span>{itemType}</span>
          </div>
        );
    }
  };

  const tabs = [
    { id: 'banner', label: '🖼️ Bannières', count: inventory.banner?.length || 0 },
    { id: 'avatar', label: '👤 Avatars', count: inventory.avatar?.length || 0 },
    { id: 'badge', label: '🏆 Badges', count: inventory.badge?.length || 0 },
    { id: 'custom_tag', label: '🏷️ Étiquettes', count: inventory.custom_tag?.length || 0 },
    { id: 'title', label: '👑 Titres', count: inventory.title?.length || 0 },
    { id: 'theme', label: '🎨 Thèmes', count: inventory.theme?.length || 0 }
  ];

  if (!isOpen) return null;

  return (
    <div className="inventory-overlay">
      <div className="inventory-modal">
        <div className="inventory-header">
          <h2>💼 Mon Inventaire</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="inventory-tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`inventory-tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
              {tab.count > 0 && <span className="tab-count">{tab.count}</span>}
            </button>
          ))}
        </div>

        <div className="inventory-content">
          {loading ? (
            <div className="loading-inventory">
              <div className="loading-spinner"></div>
              <p>Chargement de votre inventaire...</p>
            </div>
          ) : (
            <div className="items-grid">
              {inventory[activeTab]?.length === 0 ? (
                <div className="no-items">
                  <p>Aucun {tabs.find(t => t.id === activeTab)?.label.split(' ')[1].toLowerCase()} dans votre inventaire</p>
                  <p>Visitez la marketplace pour en acheter !</p>
                </div>
              ) : (
                inventory[activeTab]?.map(item => (
                  <div key={item.id} className={`inventory-item ${item.is_equipped ? 'equipped' : ''}`}>
                    <div className="item-preview">
                      {getItemPreview(item)}
                    </div>
                    
                    <div className="item-info">
                      <h4>{item.item_name}</h4>
                      <p className="item-date">
                        Acheté le {new Date(item.purchased_at).toLocaleDateString('fr-FR')}
                      </p>
                    </div>

                    <div className="item-actions">
                      {item.is_equipped ? (
                        <div className="equipped-badge">
                          ✅ Équipé
                        </div>
                      ) : (
                        <button
                          className="equip-btn"
                          onClick={() => equipItem(item.id)}
                        >
                          Équiper
                        </button>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Inventaire;