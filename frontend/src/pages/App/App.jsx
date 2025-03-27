import { useEffect, useState, useRef } from 'react';
import axios from "axios";
import renderStatsGrid from '../../utils/Renders/renderStatsGrid';
import './App.css';

function App() {
  const mountRef = useRef(false);
  const [studentId, setStudentId] = useState();
  const [json, setJson] = useState({});
  const [check, setCheck] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setCheck(false)
        // менять ссылку здесь
        await axios.get("https://jsonplaceholder.typicode.com/posts/"+studentId)
        .then(res => setJson(res))
      } catch (err) {
        setError(err);
      } finally {
        setCheck(true);
      } 
    }
    setError(null);
    if (mountRef.current) {fetchData()} else {mountRef.current = true};
  }, [studentId]);

  return (
    <>
    <div className="div-search">
      <input className='input-id' type="text" placeholder="Введите ваш СНИЛС.." style={{marginBottom: "10px"}}></input>
      <button className='div-btn' onClick={() => setStudentId(document.querySelector('.input-id').value)}>Начать поиск!</button>
    </div>

    {error ? <div className='div-error-mes' style={{minHeight:"70vh"}}> {error.message} </div>
          : check ? <div className="grid-stats"> {renderStatsGrid(json.data)} </div>
                  : <div style={{minHeight:"70vh"}}> </div>}
    </>
  );
}

export default App;
