import { useEffect, useState } from "react";
import axios from "axios";

function useAxios(url) {
  const [json, setJson] = useState([]);
  const [error, setError] = useState(null);
  const [check, setCheck] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setCheck(false)
        await axios.get(url)
        .then(res => setJson(res))
      } catch (err) {
        setError(err);
      } finally {
        setCheck(true);
      } 
    }
    fetchData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return ({
    json: json,
    error: error,
    isLoaded: check
  });
  }
  
  export default useAxios;