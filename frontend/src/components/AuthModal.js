import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const AuthModal = ({ isOpen, onClose, initialMode = 'login' }) => {
  const [mode, setMode] = useState(initialMode);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: '',
    display_name: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login, register, API_BASE_URL } = useAuth();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
    setSuccess('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (mode === 'login') {
        const result = await login(formData.email, formData.password);
        if (result.success) {
          onClose();
          setFormData({
            email: '',
            password: '',
            username: '',
            display_name: '',
            confirmPassword: ''
          });
        } else {
          setError(result.error);
        }
      } else {
        // Validation pour l'inscription
        if (formData.password !== formData.confirmPassword) {
          setError('Les mots de passe ne correspondent pas');
          setLoading(false);
          return;
        }

        if (formData.password.length < 6) {
          setError('Le mot de passe doit contenir au moins 6 caractères');
          setLoading(false);
          return;
        }

        const result = await register({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          display_name: formData.display_name
        });

        if (result.success) {
          onClose();
          setFormData({
            email: '',
            password: '',
            username: '',
            display_name: '',
            confirmPassword: ''
          });
        } else {
          setError(result.error);
        }
      }
    } catch (err) {
      setError('Une erreur inattendue s\'est produite');
    }

    setLoading(false);
  };

  const handleForgotPassword = async () => {
    if (!formData.email) {
      setError('Veuillez saisir votre adresse email');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/auth/request-password-reset?email=${encodeURIComponent(formData.email)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const result = await response.json();
        setSuccess(
          `📧 ${result.message}\n\n` +
          "Un lien de réinitialisation a été envoyé à votre adresse email. " +
          "Vérifiez votre boîte de réception et suivez les instructions pour changer votre mot de passe."
        );
        if (result.reset_link) {
          // In development, also show the reset link
          console.log('Reset link (dev):', result.reset_link);
          setSuccess(prev => prev + `\n\n🔗 Lien de développement: ${result.reset_link}`);
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la demande de réinitialisation');
      }
    } catch (error) {
      console.error('Erreur lors de la demande:', error);
      setError('Erreur lors de la demande de réinitialisation du mot de passe');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setMode(mode === 'login' ? 'register' : 'login');
    setError('');
    setSuccess('');
    setFormData({
      email: '',
      password: '',
      username: '',
      display_name: '',
      confirmPassword: ''
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>{mode === 'login' ? 'Connexion' : 'Inscription'}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          {mode === 'register' && (
            <>
              <div className="form-group">
                <label htmlFor="username">Nom d'utilisateur</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  placeholder="Votre nom d'utilisateur"
                />
              </div>

              <div className="form-group">
                <label htmlFor="display_name">Nom d'affichage</label>
                <input
                  type="text"
                  id="display_name"
                  name="display_name"
                  value={formData.display_name}
                  onChange={handleChange}
                  required
                  placeholder="Votre nom d'affichage"
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="votre@email.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Mot de passe</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Votre mot de passe"
              minLength="6"
            />
          </div>

          {mode === 'register' && (
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirmer le mot de passe</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                placeholder="Confirmez votre mot de passe"
              />
            </div>
          )}

          <button 
            type="submit" 
            className="submit-button"
            disabled={loading}
          >
            {loading ? 'Chargement...' : (mode === 'login' ? 'Se connecter' : 'S\'inscrire')}
          </button>

          {mode === 'login' && (
            <div className="forgot-password">
              <button 
                type="button" 
                className="forgot-password-btn"
                onClick={handleForgotPassword}
                disabled={loading}
              >
                🔐 Mot de passe oublié ?
              </button>
            </div>
          )}

          <div className="auth-switch">
            {mode === 'login' ? (
              <p>
                Pas encore de compte ?{' '}
                <button type="button" onClick={toggleMode} className="link-button">
                  S'inscrire
                </button>
              </p>
            ) : (
              <p>
                Déjà un compte ?{' '}
                <button type="button" onClick={toggleMode} className="link-button">
                  Se connecter
                </button>
              </p>
            )}
          </div>
        </form>
      </div>

      <style jsx>{`
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: rgba(0, 0, 0, 0.7);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }

        .modal-content {
          background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
          border-radius: 15px;
          padding: 0;
          max-width: 400px;
          width: 90%;
          max-height: 90vh;
          overflow-y: auto;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px 25px;
          border-bottom: 1px solid rgba(59, 130, 246, 0.3);
        }

        .modal-header h2 {
          color: white;
          margin: 0;
          font-size: 24px;
          font-weight: 600;
        }

        .close-button {
          background: none;
          border: none;
          color: white;
          font-size: 24px;
          cursor: pointer;
          padding: 0;
          width: 30px;
          height: 30px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: background-color 0.3s;
        }

        .close-button:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        .auth-form {
          padding: 25px;
        }

        .form-group {
          margin-bottom: 20px;
        }

        .form-group label {
          display: block;
          margin-bottom: 5px;
          color: white;
          font-weight: 500;
        }

        .form-group input {
          width: 100%;
          padding: 12px;
          border: 2px solid rgba(59, 130, 246, 0.3);
          border-radius: 8px;
          background: rgba(255, 255, 255, 0.1);
          color: white;
          font-size: 16px;
          transition: all 0.3s;
          box-sizing: border-box;
        }

        .form-group input:focus {
          outline: none;
          border-color: #3b82f6;
          background: rgba(255, 255, 255, 0.15);
        }

        .form-group input::placeholder {
          color: rgba(255, 255, 255, 0.6);
        }

        .error-message {
          background-color: rgba(239, 68, 68, 0.2);
          color: #fca5a5;
          padding: 10px;
          border-radius: 8px;
          margin-bottom: 20px;
          border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .success-message {
          background-color: rgba(34, 197, 94, 0.2);
          color: #86efac;
          padding: 10px;
          border-radius: 8px;
          margin-bottom: 20px;
          border: 1px solid rgba(34, 197, 94, 0.3);
          white-space: pre-line;
        }

        .submit-button {
          width: 100%;
          padding: 12px;
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
          margin-bottom: 20px;
        }

        .submit-button:hover:not(:disabled) {
          background: linear-gradient(45deg, #2563eb, #1e40af);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
        }

        .submit-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          transform: none;
          box-shadow: none;
        }

        .forgot-password {
          text-align: center;
          margin-bottom: 20px;
        }

        .forgot-password-btn {
          background: none;
          border: none;
          color: #60a5fa;
          cursor: pointer;
          font-size: 14px;
          transition: color 0.3s;
        }

        .forgot-password-btn:hover:not(:disabled) {
          color: #93c5fd;
        }

        .forgot-password-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .auth-switch {
          text-align: center;
          color: rgba(255, 255, 255, 0.8);
        }

        .link-button {
          background: none;
          border: none;
          color: #60a5fa;
          cursor: pointer;
          text-decoration: underline;
          font-size: inherit;
        }

        .link-button:hover {
          color: #93c5fd;
        }

        @media (max-width: 480px) {
          .modal-content {
            margin: 10px;
          }
          
          .modal-header {
            padding: 15px 20px;
          }
          
          .auth-form {
            padding: 20px;
          }
        }
      `}</style>
    </div>
  );
};

export default AuthModal;