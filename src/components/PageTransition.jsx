import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const PageTransition = ({ children }) => {
  const [displayChildren, setDisplayChildren] = useState(children);
  const [transitionStage, setTransitionStage] = useState('fadeIn');
  const location = useLocation();

  useEffect(() => {
    setTransitionStage('fadeOut');
    
    const timer = setTimeout(() => {
      setDisplayChildren(children);
      setTransitionStage('fadeIn');
    }, 300);

    return () => clearTimeout(timer);
  }, [children, location.key]);

  return (
    <div className={`page-transition ${transitionStage}`}>
      {displayChildren}
    </div>
  );
};

export default PageTransition;