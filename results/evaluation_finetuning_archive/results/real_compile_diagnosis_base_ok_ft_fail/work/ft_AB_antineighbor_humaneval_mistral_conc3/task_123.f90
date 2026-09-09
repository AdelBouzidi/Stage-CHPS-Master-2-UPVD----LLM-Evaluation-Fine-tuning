program get_odd_collatz
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read *, n
  
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
    integer :: count = 0
    
    ! Calculate Collatz sequence and count odd numbers
    temp = n
    do while (temp > 0)
      if (mod(temp, 2) == 1) then
        count = count + 1
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    
    allocate(res(count))
    i = 0
    temp = n
    do while (temp > 0)
      if (mod(temp, 2) == 1) then
        i = i + 1
        res(i) = temp
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    
  end function get_odd_collatz

end program get_odd_collatz