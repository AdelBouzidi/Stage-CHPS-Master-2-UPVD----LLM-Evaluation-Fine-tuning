program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call factorize function
  factors = factorize(n)
  
  ! Output results
  print *, factors
contains

  function factorize(n) result(factors)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: factors(:)
    integer :: i, count, temp
    
    if (n <= 1) then
      allocate(factors(0))
      return
    end if
    
    count = 0
    temp = n
    do i = 2, temp
      if (mod(temp, i) == 0) then
        count = count + 1
        temp = temp / i
      else
        exit
      end if
    end do
    
    allocate(factors(count))
    factors = [ (i, i = 1, count) ]
  end function factorize

end program factorize_demo