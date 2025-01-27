/*
 * Copyright (c) 2025 Péter Molnár
 * LinkedIn: https://www.linkedin.com/in/petermolnar/
 *
 * This code is licensed under the Creative Commons license. 
 * You are free to use, modify, and distribute it as long as proper attribution is provided.
 * 
 * Authorship: Péter Molnár with assistance from AI tools.
 * 
 * Disclaimer: This code is provided "as is", without any guarantees of correctness or functionality.
 * Use it at your own risk. The author assumes no liability for any issues arising from its use.
 * 
 */
const reportWebVitals = onPerfEntry => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;
