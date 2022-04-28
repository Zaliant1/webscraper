import React, { useEffect, useState } from "react";

import { useParams } from "react-router-dom";
import { Row, Col, Card } from "react-bootstrap";

const CastMemberComponent = () => {
  let { castmember } = useParams();
  const [castMemberData, setCastMember] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/castspecific/${castmember}/info`)
      .then((response) => response.json())
      .then((data) => {
        setCastMember(data);
        setLoading(false);
      });
  }, [castmember]);

  if (loading === true) {
    return <h2>fetching cast member details...</h2>;
  } else if (loading === false && castMemberData === null) {
    return null;
  } else if (loading === false && castMemberData !== null) {
    return (
      <Card style={{ marginTop: "15px" }}>
        <Card.Body>
          <Row>
            <Col
              key={`card-${castMemberData.title}-info`}
              md="3"
              style={{
                marginBottom: "15px",
                marginTop: "15px",
                textAlign: "center",
              }}
            >
              <img
                src={castMemberData.image}
                className="card-img-top"
                alt="..."
                border="1px solid #000"
              />
              <p>{castMemberData.name}</p>
              <p>Birthday : {castMemberData.birthday}</p>
            </Col>
            <Col
              key={`card-${castMemberData.title}-synopsis`}
              md="5"
              style={{
                marginBottom: "15px",
                marginTop: "10px",
                textAlign: "left",
              }}
            >
              <div style={{ textAlign: "center" }}>
                <h2>About {castMemberData.name}</h2>
              </div>
              <p>{castMemberData.summary}</p>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    );
  }
};

export default CastMemberComponent;
