import React from 'react';

const Home = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">Welcome to Viber</h1>
      <p className="text-lg mb-4">
        Your digital hub for connecting and communicating.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-10">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">Connect</h2>
          <p>Connect with friends, family, and colleagues instantly.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">Share</h2>
          <p>Share your moments, thoughts, and experiences with your network.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">Discover</h2>
          <p>Discover new connections and content tailored to your interests.</p>
        </div>
      </div>
    </div>
  );
};

export default Home; 