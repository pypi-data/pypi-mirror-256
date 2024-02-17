class Fraction:
    
    def __init__(self,num,den):
        self.num = int(num)
        self.den = int(den)


    def __str__(self):
        return "{}/{}".format(self.num,self.den)
    
    ## Function for the Addition Operation ##

    def __add__(self,other):

        temp_num = self.num*other.den + other.num*self.den
        temp_den = self.den*other.den

        if temp_num==0 or temp_den==0:
            return self.__zero_handler(temp_num,temp_den)
        else:
            cf = self.__compute_hcf(temp_num,temp_den)
            simp_num = int(temp_num/cf)
            simp_den = int(temp_den/cf)

        return self.__return_func(simp_num,simp_den)
    
    ## Function for the Subtraction Operation ##

    def __sub__(self,other):

        temp_num = self.num*other.den - other.num*self.den
        temp_den = self.den*other.den

        if temp_num==0 or temp_den==0:
            return self.__zero_handler(temp_num,temp_den)
        else:
            cf = self.__compute_hcf(temp_num,temp_den)
            simp_num = int(temp_num/cf)
            simp_den = int(temp_den/cf)

        return self.__return_func(simp_num,simp_den)
    
    ## Function for the Multiplication Operation ##

    def __mul__(self,other):

        temp_num = self.num*other.num
        temp_den = self.den*other.den

        if temp_num==0 or temp_den==0:
            return self.__zero_handler(temp_num,temp_den)
        else:
            cf = self.__compute_hcf(temp_num,temp_den)
            simp_num = int(temp_num/cf)
            simp_den = int(temp_den/cf)

        return self.__return_func(simp_num,simp_den)
    
    ## Function for the Division Operation ##

    def __truediv__(self,other):
        temp_num = self.num*other.den
        temp_den = self.den*other.num

        if temp_num==0 or temp_den==0:
            return self.__zero_handler(temp_num,temp_den)
        else:
            cf = self.__compute_hcf(temp_num,temp_den)
            simp_num = int(temp_num/cf)
            simp_den = int(temp_den/cf)

        return self.__return_func(simp_num,simp_den)
        
    ## Function for Calculating the HCF ##

    def __compute_hcf(self,x,y):

        if x > y :
            smaller = y
        else:
            smaller = x
        
        for i in range(1,smaller+1):
            if((x%i == 0) and (y%i ==0)):
                hcf = i

        return hcf
    
    ## Common Function for Return ##
    def __return_func(self,num,den):

        if num == den:
            return 1      
        elif den == 1:
            return num
        else:
            # return "{}/{}".format(num,den)
            return Fraction(num,den)
    
    ## Function for Handling zeros ##
    def __zero_handler(self,num,den):

        if num == 0:
            return 0
        if den == 0:
            return "Error!!"