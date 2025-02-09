import { useAuth0 } from "@auth0/auth0-react";

const Profile = () => {
  const { user, isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <div>Loading ...</div>;
  }

  return (
    isAuthenticated && (
      <div className="bg-white/10 backdrop-blur-lg p-8 rounded-xl max-w-2xl mx-auto">
        <div className="flex items-center gap-6 mb-8">
          <img 
            src={user?.picture} 
            alt={user?.name} 
            className="rounded-full w-24 h-24 border-4 border-cyan-500"
          />
          <div>
            <h2 className="text-3xl font-bold text-white">{user?.name}</h2>
            <p className="text-gray-300">{user?.email}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white/5 p-4 rounded-lg">
            <p className="text-gray-400">User ID</p>
            <p className="text-white font-mono text-sm">{user?.sub}</p>
          </div>
          <div className="bg-white/5 p-4 rounded-lg">
            <p className="text-gray-400">Email Verified</p>
            <p className="text-white">{user?.email_verified ? 'Yes' : 'No'}</p>
          </div>
        </div>
      </div>
    )
  );
};

export default Profile; 