import React, { useState } from "react";
import { Card, CardContent } from "./componments/ui/card";
import { Button } from "./componments/ui/button";

const BananaChecker = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  //Check file type, make sure it is an image
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    const allowTypes = ['image/jpeg','image/png','image/gif','image/webp','image/jpg'];
    if (file){
      if (!allowTypes.includes(file.type)){
        alert("Only allow submit image(png, jpg, jpeg, gif, and webp form).");
        return;
      }
      setSelectedFile(file);
      //Reset the result when use upload a new file
      setResult(null)
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert("Please submit a image:");
      return;
    }

    setIsLoading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/api/Banana_ripeness_status_identification", {
        method: "POST",
        body: formData,
        mode: "cors",
        headers: {
          "Access-Control-Allow-Origin": "http://localhost:5173",
        },
      });

      if (!response.ok) {
        throw new Error("Can't process this image");
      }

      const back = await response.json();

      //Check result and show result
      if (back.status){
        setResult(`This banana is ${back.Status}`);
      }else if (back.error){
        setResult(`This banana is ${back.Status}`);
      }else {
        setResult("Can't analysis image.")
      }

    } catch (error) {
      console.error(error);
      setResult("Error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-md">
        <CardContent className="flex flex-col gap-4">
          <h1 className="text-xl font-bold text-center">Banana ripeness status identification</h1>

          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="file-input"
          />

          <Button onClick={handleSubmit} disabled={isLoading} className="w-full">
            {isLoading ? "Testing..." : "Submit"}
          </Button>

          {result && (
            <div className="mt-4 text-center text-lg font-semibold">
              {result}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default BananaChecker;