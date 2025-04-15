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

function App() {
  const [loading, setLoading] = useState(true);
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
      setTimeout(() => {
        setShowContent(true);
      }, 300);
    }, 1000);
  }, []);

  return (
    <>
      {loading ? (
        <Loading />
      ) : (
        <div className={`app-content ${showContent ? "fade-in" : ""}`}>
          <Router>
            <ScrollToTop/>
            <Navbar />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/book-ambulance" element={<BookAmbulance/>}/>
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/signin" element={<Signin/>}/>
            </Routes>
            <Footer/>
          </Router>
        </div>
      )}
    </>
  );
}

export default App;
