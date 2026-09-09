program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call factorize function
  factors = factorize(n)
  
  ! Output result
  print *, factors
contains

  function factorize(n) result(factors)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: factors(:)
    integer :: i, count
    integer :: temp
    
    if (n <= 1) then
      allocate(factors(0))
      return
    end if
    
    allocate(factors(0))
    temp = n
    
    do i = 2, temp
      count = 0
      do while (mod(temp, i) == 0)
        count = count + 1
        temp = temp / i
      end do
      if (count > 0) then
        allocate(factors(size(factors) + count))
        factors(size(factors)+1:size(factors)+count) = i
      end if
      if (temp == 1) exit
    end do
    
  end function factorize

end program factorize_demo