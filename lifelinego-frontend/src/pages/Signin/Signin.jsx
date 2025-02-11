import React, { useState } from "react";
import "./Signin.css";
import images from "../../assets/image";

const Signin = () => {
  const [isSignUp, setIsSignUp] = useState(false);

  return (
    <div className={`auth-container ${isSignUp ? "signup-mode" : "signin-mode"}`}>
      <div className="auth-left">
        <img
          src={isSignUp ? images.Signup : images.Signin}
          alt={isSignUp ? "Sign Up" : "Sign In"}
        />
      </div>
      
      {/* Right Section */}
      <div className="auth-right">
        <div className="auth-box">
          <h2>{isSignUp ? "Create an Account" : "Welcome Back"}</h2>
          <form>
            {isSignUp && <input type="text" placeholder="Full Name" required />}
            <input type="email" placeholder="Email" required />
            <input type="password" placeholder="Password" required />
            <button type="submit">{isSignUp ? "Sign Up" : "Sign In"}</button>
          </form>
          <p>
            {isSignUp ? "Already have an account? " : "Don't have an account? "}
            <span onClick={() => setIsSignUp(!isSignUp)}>
              {isSignUp ? "Sign In" : "Sign Up"}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signin;