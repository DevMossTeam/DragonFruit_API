'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDragon, faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';

export default function Login() {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  
  const router = useRouter();

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Login form submitted:', formData);
    
    // Simulate successful login
    // In real app, you'd validate credentials with API
    localStorage.setItem('token', 'fake-jwt-token');
    router.push('/dashboard'); // Redirect to dashboard after login
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-screen flex">
      {/* Left side - Form */}
      <div className="w-full lg:w-1/2 p-8 lg:p-16 flex flex-col justify-center bg-white">
        {/* Back to dashboard link
        <a href="/dashboard" className="text-gray-500 hover:text-gray-700 text-sm mb-12 flex items-center">
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to dashboard
        </a> */}

        {/* Form content */}
        <div className="max-w-md mx-auto w-full">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Sign In</h1>
          <p className="text-gray-500 mb-8">Enter your email and password to sign in!</p>

          {/* Divider */}
          {/* <div className="flex items-center mb-6">
            <div className="flex-grow border-t border-gray-200"></div>
            <span className="px-4 text-gray-500 text-sm">Or</span>
            <div className="flex-grow border-t border-gray-200"></div>
          </div> */}

          {/* Email field */}
          <div className="mb-6 text-black">
            <label className="block text-sm font-medium text-gray-700 mb-2">Email<span className="text-red-500">*</span></label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="info@gmail.com"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>

          {/* Password field */}
          <div className="mb-6 text-black">
            <label className="block text-sm font-medium text-gray-700 mb-2">Password<span className="text-red-500">*</span></label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
              >
                {showPassword ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 012.557-5.372A9.97 9.97 0 015.057 5.372a9.97 9.97 0 012.557-5.372A10.05 10.05 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.05 10.05 0 01-5.372 5.372z" />
                  </svg>
                )}
              </button>
            </div>
          </div>

            {/* Password field */}
            <div className="mb-6 text-black">
              <label className="block text-sm font-medium text-gray-700 mb-2">Password<span className="text-red-500">*</span></label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  required
                  disabled={loading}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition disabled:opacity-50 disabled:cursor-not-allowed"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={loading}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 disabled:opacity-50"
                >
                  <FontAwesomeIcon
                    icon={showPassword ? faEyeSlash : faEye}
                    className="w-5 h-5"
                  />
                </button>
              </div>
            </div>

            {/* Remember me and forgot password */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700">
                  Keep me logged in
                </label>
              </div>
              <a href="#" className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                Forgot password?
              </a>
          {/* Remember me and forgot password */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <input
                id="remember-me"
                type="checkbox"
                className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700">
                Keep me logged in
              </label>
            </div>
            <a href="#" className="text-sm text-blue-600 hover:text-blue-800 font-medium">
              Forgot password?
            </a>
          </div>

          {/* Sign in button */}
          <button
            type="submit"
            onClick={handleSubmit}
            className="w-full py-3 px-4 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Sign In
          </button>

          {/* Sign up link */}
          <p className="mt-6 text-sm text-gray-600 text-center">
            Don't have an account?{' '}
            <a href="#" className="text-blue-600 hover:text-blue-800 font-medium">
              Sign Up
            </a>
          </p>
        </div>
      </div>

      {/* Right side - Branding */}
      <div className="hidden lg:block w-1/2 bg-pink-900 relative overflow-hidden">
        {/* Grid pattern background */}
        <div className="absolute inset-0 opacity-20">
          <div className="grid grid-cols-12 gap-4 h-full">
            {Array.from({ length: 48 }).map((_, i) => (
              <div key={i} className="bg-pink-500 rounded-sm"></div>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center p-16 text-white">
          <div className="flex items-center mb-6">
            <div className="w-12 h-12 bg-red-500 rounded-lg flex items-center justify-center mr-4">
                <FontAwesomeIcon 
                icon={faDragon} 
                className="text-[30px] text-gray-800 dark:text-white" 
                aria-hidden="true"/>
            </div>
            <h2 className="text-4xl font-bold">DragonFruit</h2>
          </div>
          <p className="text-xl text-center max-w-md">
             Sistem Grading Buah Naga Super Merah (Hylocereus Costaricensis) Berbasis Pengolahan Citra Digital dan Fuzzy Logic Terintegrasi dengan Embedded System
          </p>
        </div>

        {/* Dark mode toggle */}
        {/* <button className="absolute bottom-6 right-6 w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white hover:bg-blue-700 transition-colors">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0112 21a9.003 9.003 0 018.354-5.646z" />
          </svg>
        </button> */}
      </div>
    </div>
  );
}