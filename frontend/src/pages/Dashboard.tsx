import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import UploadBox from '../components/UploadBox';
import TopicInput from '../components/TopicInput';
import StudyStreak from '../components/StudyStreak';
import StudyCalendar from '../components/StudyCalendar';
import { historyApi } from '../api/history';
import { HistoryEntry } from '../types/api';
import { LEARNER_ID } from '../App';

const Dashboard = () => {
  const navigate = useNavigate();
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await historyApi.getHistory(LEARNER_ID);
        setHistory(response.history);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const handleLearn = (topic: string) => {
    navigate(`/learn?topic=${encodeURIComponent(topic)}`);
  };

  return (
    <div className="flex flex-col space-y-12 pb-24 md:pb-8">
      {/* Hero Section */}
      <section className="text-center space-y-6 pt-8">
        <span className="text-sm font-bold tracking-widest text-indigo-600 uppercase">Personalized Learning</span>
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight leading-tight">
          Learn from what you already know.
        </h1>
        <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto font-light">
          Your learning path adapts to your existing knowledge, study material, and goals.
        </p>
        
        <div className="max-w-2xl mx-auto mt-10 bg-white p-6 md:p-8 rounded-3xl shadow-lg shadow-indigo-100/50 border border-gray-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-blue-500 to-indigo-500"></div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">What do you want to learn?</h2>
          <TopicInput onSubmit={handleLearn} />
        </div>
      </section>

      {/* Progress Section */}
      {!isLoading && history.length > 0 && (
        <section className="max-w-4xl mx-auto w-full grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1">
            <StudyStreak history={history} />
          </div>
          <div className="md:col-span-2">
            <StudyCalendar history={history} />
          </div>
        </section>
      )}

      {/* Upload Section */}
      <section className="max-w-4xl mx-auto w-full">
        <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload your notes</h2>
            <p className="text-gray-600">Your study material becomes part of your personal knowledge base.</p>
          </div>
          <UploadBox />
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
