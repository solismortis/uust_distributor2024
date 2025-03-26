import { Outlet } from 'react-router-dom';
import Header from './Header/Header';
import Footer from './Footer/Footer';
import Sidebar from './Sidebar/Sidebar';

function Layout() {
  return (
    <>
      <Header />
      <Sidebar />
      <div className="main">
        <Outlet />
      </div>
      <Footer />
    </>
  );
}

export default Layout;