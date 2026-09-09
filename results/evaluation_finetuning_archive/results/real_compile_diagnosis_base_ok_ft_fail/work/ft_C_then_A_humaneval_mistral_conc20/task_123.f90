program get_odd_collatz
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Print output
  print *, result
contains
  function get_odd_collatz(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    logical :: first
    
    temp = n
    first = .true.
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        if (first) then
          allocate(res(1))
          res(1) = temp
          first = .false.
        else
          allocate(res(size(res)+1))
          res(size(res)) = temp
        end if
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
  end function get_odd_collatz
end program get_odd_collatz