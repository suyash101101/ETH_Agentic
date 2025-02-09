import { useAuth0 } from '@auth0/auth0-react';
import Profile from './components/Profile';
import LoginButton from './components/LoginButton';
import LogoutButton from './components/LogoutButton';

function App() {
  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900">
      {!isAuthenticated ? (
        <div className="container mx-auto px-6 py-16 flex flex-col items-center">
          <h1 className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500 mb-8 text-center">
            Welcome to BlockBlend
          </h1>
          <p className="text-xl text-gray-300 text-center max-w-2xl mb-12">
            Transform your traditional applications into Web3 solutions with AI-powered tools and zero-knowledge proofs
          </p>
          <LoginButton />
        </div>
      ) : (
        <div className="container mx-auto px-6 py-12">
          <div className="flex justify-end mb-8">
            <LogoutButton />
          </div>
          <Profile />
        </div>
      )}
    </div>
  );
}

export default App;