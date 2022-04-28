import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Container } from "react-bootstrap";

const SearchBox = () => {
  let navigate = useNavigate();
  let { title } = useParams();

  const [inputTitle, setTitle] = useState(title || "");

  const inputHandle = (e) => {
    setTitle(e.target.value);
  };

  const submitHandle = () => {
    navigate(`/search/${inputTitle}`);
    // Redirect;
  };

  useEffect(() => {
    const listener = (e) => {
      if (e.code === "Enter" || e.code === "NumpadEnter") {
        e.preventDefault();
        submitHandle();
      }
    };
    document.addEventListener("keydown", listener);
    return () => {
      document.removeEventListener("keydown", listener);
    };
  });

  return (
    <Container fluid="md">
      <input type="text" value={inputTitle} onChange={inputHandle} />
      <button onClick={submitHandle}>Search</button>
    </Container>
  );
};

export default SearchBox;
