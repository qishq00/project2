'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';

interface Post {
  slug: string;
  title: string;
  author: string;
  date: string;
  category: string;
}

// Make sure this URL matches your backend API route and the backend server is running
const API_URL = 'http://localhost:8000/api/posts';

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get(API_URL);
        setPosts(response.data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);

  return (
    <main className="flex flex-col items-center min-h-screen bg-gray-100 p-8">
      <div className="w-full max-w-2xl">
        <h1 className="text-5xl font-bold mb-8 text-center text-gray-800">
          Минималистичный Блог
        </h1>
        {loading ? (
          <p>Загрузка постов...</p>
        ) : (
          <div className="space-y-8">
            {Object.entries(
              posts.reduce((acc, post) => {
                if (!acc[post.category]) acc[post.category] = [];
                acc[post.category].push(post);
                return acc;
              }, {} as Record<string, Post[]>)
            ).map(([category, catPosts]) => (
              <div key={category}>
                <h2 className="text-xl font-bold text-gray-700 mb-2">{category}</h2>
                <div className="space-y-4">
                  {catPosts.map((post) => (
                    <Link
                      key={post.slug}
                      href={`/posts/${post.slug}`}
                      className="block p-6 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow"
                    >
                      <h3 className="text-2xl font-semibold text-blue-600">{post.title}</h3>
                      <div className="text-sm text-gray-500 mt-1">
                        Автор: {post.author} | Дата: {post.date}
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}