function useLocalStorage({method, name, value}) {
  switch (method) {
    case "GET":
      return localStorage.getItem(name);
    case "POST":
      return localStorage.setItem(name, value);
    case "DELETE":
      return localStorage.removeItem(name);

    default:
      return "error";
  }
}

export default useLocalStorage;