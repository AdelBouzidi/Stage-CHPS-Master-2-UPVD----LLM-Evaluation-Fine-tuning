program factorize_demo
  implicit none
  integer, allocatable :: factors(:)
  integer :: n
  
  ! Read input
  read(*,*) n
  
  ! Call the factorize function
  factors = factorize(n)
  
  ! Print output
  print *, factors
  
contains

  function factorize(n) result(factors)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: factors(:)
    integer :: i, temp
    
    if (n <= 1) then
      allocate(factors(0))
      return
    end if
    
    allocate(factors(0))
    temp = n
    i = 2
    do while (temp > 1)
      if (mod(temp, i) == 0) then
        factors = [factors, i]
        temp = temp / i
      else
        i = i + 1
      end if
    end do
  end function factorize

end program factorize_demo