program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the factorize function
  factors = factorize(n)
  
  ! Output the result
  print *, factors
contains

  function factorize(n) result(factors)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: factors(:)
    integer :: i, count, idx
    
    if (n <= 1) then
      allocate(factors(0))
      return
    end if
    
    allocate(factors(0))
    do i = 2, n
      count = 0
      do while (mod(n, i) == 0)
        count = count + 1
        n = n / i
      end do
      if (count > 0) then
        allocate(factors(size(factors) + count))
        factors(size(factors)+1:size(factors)+count) = i
      end if
      if (n == 1) exit
    end do
  end function factorize

end program factorize_demo