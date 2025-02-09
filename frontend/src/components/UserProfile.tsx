import { useAuth0 } from '@auth0/auth0-react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

interface UserMetadata {
  created_at: string;
  last_login: string;
  login_count: number;
}

const UserProfile = () => {
  const { user, getAccessTokenSilently } = useAuth0();
  const [userMetadata, setUserMetadata] = useState<UserMetadata | null>(null);

  useEffect(() => {
    const getUserMetadata = async () => {
      try {
        const accessToken = await getAccessTokenSilently();
        const userDetailsByIdUrl = `https://${import.meta.env.VITE_AUTH0_DOMAIN}/api/v2/users/${user?.sub}`;

        const metadataResponse = await fetch(userDetailsByIdUrl, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        const metadata = await metadataResponse.json();
        setUserMetadata(metadata);
      } catch (error) {
        console.error('Error fetching user metadata:', error);
      }
    };

    if (user?.sub) {
      getUserMetadata();
    }
  }, [getAccessTokenSilently, user?.sub]);

  return (
    <div className="min-h-screen p-6">
      <nav className="flex justify-between items-center mb-8">
        <Link 
          to="/dashboard"
          className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500"
        >
          BlockBlend
        </Link>
      </nav>

      <div className="max-w-4xl mx-auto">
        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 mb-8">
          <div className="flex items-center gap-6 mb-8">
            {user?.picture && (
              <img 
                src={user.picture} 
                alt="Profile" 
                className="w-24 h-24 rounded-full border-4 border-cyan-500"
              />
            )}
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">{user?.name}</h1>
              <p className="text-gray-300">{user?.email}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white/5 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-3">Basic Information</h3>
              <div className="space-y-2">
                <p className="text-gray-300">
                  <span className="text-gray-400">User ID: </span>
                  {user?.sub}
                </p>
                <p className="text-gray-300">
                  <span className="text-gray-400">Nickname: </span>
                  {user?.nickname}
                </p>
                <p className="text-gray-300">
                  <span className="text-gray-400">Email Verified: </span>
                  {user?.email_verified ? 'Yes' : 'No'}
                </p>
              </div>
            </div>

            <div className="bg-white/5 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-3">Account Details</h3>
              <div className="space-y-2">
                <p className="text-gray-300">
                  <span className="text-gray-400">Created: </span>
                  {userMetadata?.created_at && new Date(userMetadata.created_at).toLocaleDateString()}
                </p>
                <p className="text-gray-300">
                  <span className="text-gray-400">Last Login: </span>
                  {userMetadata?.last_login && new Date(userMetadata.last_login).toLocaleDateString()}
                </p>
                <p className="text-gray-300">
                  <span className="text-gray-400">Login Count: </span>
                  {userMetadata?.login_count}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile; 