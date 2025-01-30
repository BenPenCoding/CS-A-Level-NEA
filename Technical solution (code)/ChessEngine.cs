Using System;

namespace ChessEngine {
  
  class Program {

    class Entity {
      private string pName;
      public string name {
        get {return pName;}
        set {pName = value;}
      }

      private int[] pHeatTol;
      public int[] heatTol {
        get {return pHeatTol;}
        set {pHeatTol = value;}

      }

    }
    void static Main(string[] args){
      Console.WriteLine("Hello!");
    }
  

  }
  

}
  
