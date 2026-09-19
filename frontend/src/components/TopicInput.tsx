import { useState } from 'react';
import { ArrowRight } from 'lucide-react';

interface TopicInputProps {
  onSubmit: (topic: string) => void;
  initialValue?: string;
  isLoading?: boolean;
}

const TopicInput = ({ onSubmit, initialValue = '', isLoading = false }: TopicInputProps) => {
  const [topic, setTopic] = useState(initialValue);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim() && !isLoading) {
      onSubmit(topic.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-center gap-4">
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Teach me LRU Cache..."
        className="w-full flex-1 px-6 py-4 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-lg shadow-sm placeholder:text-gray-400"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={!topic.trim() || isLoading}
        className="w-full sm:w-auto px-8 py-4 bg-indigo-600 text-white rounded-xl font-bold text-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg flex items-center justify-center whitespace-nowrap"
      >
        {isLoading ? 'Starting...' : 'Start Learning'}
        {!isLoading && <ArrowRight className="ml-2 h-5 w-5" />}
      </button>
    </form>
  );
};

export default TopicInput;
