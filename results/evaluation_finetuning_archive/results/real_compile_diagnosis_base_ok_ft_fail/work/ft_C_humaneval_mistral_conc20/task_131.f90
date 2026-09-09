program digits
  implicit none
  integer :: n, result, digit
  result = 0
  
  read(*,*) n
  
  do while (n > 0)
    digit = mod(n, 10)
    if (digit /= 0 .and. digit /= 2 .and. digit /= 4 .and. digit /= 6 .and. digit /= 8) then
      result = result * digit
    end if
    n = n / 10
  end do
  
  print *, result
end program digits