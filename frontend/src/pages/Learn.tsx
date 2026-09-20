import { useEffect, useState, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { learningApi } from '../api/learning';
import { LEARNER_ID } from '../App';
import { Loader2 } from 'lucide-react';
import LessonView from '../components/LessonView';
import { LearningResponse } from '../types/api';

const Learn = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const topic = searchParams.get('topic');
  
  const [lessonData, setLessonData] = useState<LearningResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const lastFetchedTopic = useRef<string | null>(null);

  useEffect(() => {
    if (!topic) {
      navigate('/');
      return;
    }

    const fetchLesson = async () => {
      if (lastFetchedTopic.current === topic) return;
      lastFetchedTopic.current = topic;
      
      setIsLoading(true);
      setError(null);
      setLessonData(null);
      
      try {
        const response = await learningApi.teach({
          learner_id: LEARNER_ID,
          topic: topic,
          use_previous_material: true
        });
        setLessonData(response);
      } catch (err: any) {
        console.error(err);
        const msg = err.response?.data?.detail || 'Unable to connect to the learning engine. Make sure the FastAPI backend is running on http://127.0.0.1:8000';
        setError(msg);
      } finally {
        setIsLoading(false);
      }
    };

    fetchLesson();
  }, [topic, navigate]);

  if (error) {
    return (
      <div className="py-20 flex flex-col items-center text-center">
        <div className="bg-red-50 p-8 rounded-2xl max-w-lg border border-red-100">
          <h2 className="text-2xl font-bold text-red-900 mb-4">Error</h2>
          <p className="text-red-700 whitespace-pre-line">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="mt-6 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  if (isLoading || !lessonData) {
    return (
      <div className="py-32 flex flex-col items-center justify-center space-y-12">
        <div className="relative">
          <div className="absolute inset-0 bg-indigo-500 rounded-full blur-xl opacity-20 animate-pulse"></div>
          <Loader2 className="h-20 w-20 text-indigo-600 animate-spin relative z-10" />
        </div>
        <div className="text-center space-y-4 max-w-sm">
          <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">Crafting your lesson...</h2>
          <div className="space-y-3 text-sm font-medium text-gray-500">
            <p className="animate-pulse">Understanding the topic...</p>
            <p className="animate-pulse delay-75">Checking your knowledge base...</p>
            <p className="animate-pulse delay-150">Retrieving study material...</p>
            <p className="animate-pulse delay-300">Generating personalized lesson...</p>
          </div>
        </div>
      </div>
    );
  }

  return <LessonView lessonData={lessonData} topic={topic || ''} />;
};

export default Learn;
