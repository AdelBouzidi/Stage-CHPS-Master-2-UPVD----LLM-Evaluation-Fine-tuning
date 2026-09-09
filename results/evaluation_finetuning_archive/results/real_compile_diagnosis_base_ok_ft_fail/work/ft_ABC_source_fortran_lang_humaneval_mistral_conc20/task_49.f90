program modp
  implicit none
  integer :: n, p, result
  
  ! Read n and p from input
  read *, n
  read *, p
  
  ! Compute 2^n mod p using modular exponentiation
  result = 1
  do while (n > 0)
    if (mod(n, 2) == 1) then
      result = mod(result * 2, p)
    end if
    n = n / 2
  end do
  
  ! Output the result
  write (*, *) result
end program modp