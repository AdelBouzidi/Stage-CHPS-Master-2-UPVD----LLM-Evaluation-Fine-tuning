program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = f(n)
  
  ! Output the result
  write(*,*) result
contains

  function f(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i
    
    allocate(res(n))
    do i = 1, n
      if (mod(i, 2) == 0) then
        res(i) = factorial(i)
      else
        res(i) = sum_to(i)
      end if
    end do
  end function f

  function factorial(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res, i
    res = 1
    do i = 1, n
      res = res * i
    end do
  end function factorial

  function sum_to(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res, i
    res = 0
    do i = 1, n
      res = res + i
    end do
  end function sum_to

end program main