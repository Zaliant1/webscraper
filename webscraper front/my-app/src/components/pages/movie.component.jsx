import React, { useEffect, useState } from "react";
import { CardList } from "../card-list/cards-list";
// import { SearchBox } from "../search bar/searchbar";
import { useParams } from "react-router-dom";
import { Container, Row } from "react-bootstrap";
import { CastMemberCard } from "../card-list/cards";

const MovieComponent = () => {
  let { title } = useParams();
  const [movies, setMovies] = useState([]);
  const [castMember, setCastMember] = useState(null);

  const [loading1, setLoading1] = useState(true);
  const [loading2, setLoading2] = useState(true);

  // useEffect = () => {
  //   const CollectionRef = collection(db, "Movies");
  //   const payload = { movies };

  //   addDoc(CollectionRef, payload);
  // };

  useEffect(() => {
    // fetchMovies();
    setLoading1(true);
    setLoading2(true);
    setCastMember(null);

    fetch(`/movies/${title}/`)
      .then((response) => response.json())
      .then((data) => {
        let titles = data.map((movie) => {
          return movie;
        });
        setMovies(titles);
        setLoading1(false);
      });

    fetch(`/cast/${title}/info`)
      .then((response) => response.json())
      .then((data) => {
        setCastMember(data);
        setLoading2(false);
      });
  }, [title]);

  const Loading = () => {
    let text = "Searching for Movies & Cast";

    if (!loading1 && loading2) {
      text = "Searching for Cast";
    } else if (loading1 && !loading2) {
      text = "Searching for Movies";
    }

    return (
      <div>
        <h3>{text}</h3>
        <img
          src="https://c.tenor.com/I6kN-6X7nhAAAAAj/loading-buffering.gif"
          width={50}
          height={50}
          alt=""
        ></img>
      </div>
    );
  };

  return (
    <Container fluid="md">
      <Row>
        {loading1 || loading2 ? <Loading /> : null}
        {loading2 ? null : <CastMemberCard celeb={castMember} />}
        {!loading1 ? <CardList movies={movies} /> : null}
      </Row>
    </Container>
  );
};
// };

export default MovieComponent;
