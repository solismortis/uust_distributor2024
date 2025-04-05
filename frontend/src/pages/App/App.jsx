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
        await axios.get("http://127.0.0.1:5000/search?id="+studentId)
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

    {error ? <div style={{minHeight:"70vh"}}> {error.message} </div>
          : check ? <> {renderStatsGrid(json.data)} </>
                  : <div style={{minHeight:"70vh"}}> </div>}
    </>
  );
}

export default App;
