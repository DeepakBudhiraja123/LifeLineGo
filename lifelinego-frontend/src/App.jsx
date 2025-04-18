import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Loading from "./components/Loading/Loading";
import "./index.css";
import Home from "./pages/Home/Home";
import About from "./pages/About/About";
import Contact from "./pages/Contact/Contact";
import Navbar from "./components/Navbar/Navbar";
import Signin from "./pages/Signin/Signin";
import Footer from "./components/Footer/Footer";
import ScrollToTop from "./components/ScrollToTop/ScrollToTop";
import BookAmbulance from "./pages/BookAmbulance/BookAmbulance";
import ContactPopUp from "./components/ContactPopUp/ContactPopUp";

function App() {
  const [loading, setLoading] = useState(true);
  const [showContent, setShowContent] = useState(false);
  const [isCallModalOpen, setIsCallModalOpen] = useState(false); // Modal state

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
      setTimeout(() => {
        setShowContent(true);
      }, 300);
    }, 1000);
  }, []);

  // Open modal function
  const openCallModal = () => setIsCallModalOpen(true);

  // Close modal function
  const closeCallModal = () => setIsCallModalOpen(false);

  return (
    <>
      {loading ? (
        <Loading />
      ) : (
        <div className={`app-content ${showContent ? "fade-in" : ""}`}>
          <Router>
            <ScrollToTop />
            <Navbar openCallModal={openCallModal} />
            <Routes>
              <Route path="/" element={<Home onCallClick={openCallModal} />} />
              <Route
                path="/book-ambulance"
                element={<BookAmbulance openCallModal={openCallModal} />}
              />
              <Route path="/about" element={<About onCallClick={openCallModal} />} />
              <Route path="/signin" element={<Signin onCallClick={openCallModal} />} />
            </Routes>
            <Footer openCallModal={openCallModal}/>
          </Router>
          {/* Modal for calling */}
          <ContactPopUp isOpen={isCallModalOpen} onClose={closeCallModal} />
        </div>
      )}
    </>
  );
}

export default App;
